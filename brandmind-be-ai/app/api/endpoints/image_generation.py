from fastapi.responses import JSONResponse
from app.utils.content_generation_utils import TextRefine
from app.utils.image_generation_utils import dalle_image_generation,encode_image,image_caption,generate_caption
from app.utils.aws_utils import upload_base64_image_to_s3
from app.schemas.image_generation_schema import Refined_Prompt
from fastapi import APIRouter , File, UploadFile
import logging
from fastapi import HTTPException, status
from openai import OpenAI
import requests
import concurrent.futures
from dotenv import load_dotenv
load_dotenv()


client = OpenAI()


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('brand_mind.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)
image_generation_router = APIRouter()
    
@image_generation_router.post("/brandmind/content-image-generation")
async def text_refine_and_image_generation(prompt:Refined_Prompt):
    try:
        companyinfo=None
        impure_prompt=prompt.description
        company_id=prompt.company_id
        brand_id=prompt.brand_id
        if company_id!=0 and brand_id!=0:
            try:
                url = f"https://brandmindbe.xeventechnologies.com/api/companyManagement/getAllCompanyInformation?companyId={company_id}&brandId={brand_id}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                companyinfo=data['data']
            except Exception as e:
                return JSONResponse(content={"succeeded": False, "message": "Company information not retrieved successfully", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND)
        refined_prompt=TextRefine(impure_prompt,str(companyinfo))
        generated_image=dalle_image_generation(refined_prompt)
        s3_object_name,image_url=upload_base64_image_to_s3(generated_image)
        res={"user_prompt":impure_prompt,"image_url":image_url,"image_object_name":s3_object_name}
        # images_base64 = convert_image_url_to_base64(generated_image)
        logger.info("Response has been send")
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully genrerated refined content_and image ", "httpStatusCode": status.HTTP_200_OK, "data":res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.critical(f"Failed to genrerate refined content_and image :{e}")
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
    

@image_generation_router.post("/brandmind/multi-image-generation")
async def image_prompt_and_generation(prompt:Refined_Prompt):
    try:
        # images_list=[]
        # image_url_list=[]
        companyinfo=None
        topic = prompt.description
        company_id=prompt.company_id
        brand_id=prompt.brand_id
        if company_id!=0 and brand_id!=0:
            try:
                url = f"https://brandmindbe.xeventechnologies.com/api/companyManagement/getAllCompanyInformation?companyId={company_id}&brandId={brand_id}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                companyinfo=data['data']
            except Exception as e:
                return JSONResponse(content={"succeeded": False, "message": "Company information not retrieved successfully", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND)
        logger.info(f"User Id: {topic}")
        prompt_list=[]
        for i in range(3):
            refined_prompt=TextRefine(topic,str(companyinfo))
            prompt_list.append(refined_prompt)
        def process_prompt(refined_prompt):
            generated_image = dalle_image_generation(refined_prompt)
            s3_object_name, image_url_multi = upload_base64_image_to_s3(generated_image)
            return s3_object_name, image_url_multi
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_prompt, prompt_list)
        image_data = list(results)
        images_list = [item[0] for item in image_data]
        image_url_list = [item[1] for item in image_data]
        # for i in range(3):
        #     refined_prompt=TextRefine(topic,companyinfo)
        #     generated_image=dalle_image_generation(refined_prompt)
        #     s3_object_name,image_url=upload_base64_image_to_s3(generated_image)
        #     image_url_list.append(image_url)
        #     images_list.append(s3_object_name)
        res={"user_prompt":topic,"images_object_list":images_list,"image_url_list":image_url_list}
        logger.info("response has been send")
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully Images Generated", "httpStatusCode": status.HTTP_200_OK, "data": res   },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.critical(f"Failed to generate images: {e}")
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )



# @image_generation_router.post("/brandmind/image-caption-generation")
async def image_caption_generation(file: UploadFile = File(...)):
    try:
        logger.info(f"file content: {file}")
        base_image = encode_image(file)
        analyze_image_text= image_caption(base_image)
        caption = generate_caption(analyze_image_text)
        logger.info("caption generated succesfully ")

        return JSONResponse(
            content={
                "succeeded": True, 
                "message": "Successfully generated image description",
                "httpStatusCode": status.HTTP_200_OK, 
                "data": {"caption":caption}
            },
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
            logger.critical(f"Failed to generate caption : {e}")
            return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
