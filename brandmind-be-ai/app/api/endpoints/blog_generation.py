from fastapi.responses import JSONResponse
from app.utils.blog_utils import generate_Blog_Structure,generate_Blog_Content,generate_Blog_title
from app.utils.image_generation_utils import dalle_image_generation,blogMultiPromptGenerator
from app.utils.aws_utils import upload_base64_image_to_s3
from app.utils.content_generation_utils import marketing_info_summerizer,brand_info_summerizer,company_info_summerizer
from app.schemas.blog_schema import BlogContent,BlogTitle,BlogImages
from fastapi import APIRouter
import logging
import requests
import concurrent.futures
from fastapi import status


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('brand_mind.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


blog_generation_router = APIRouter()

@blog_generation_router.post("/brandmind/generate-titles")
async def generate_titles(data:BlogTitle):
    try:
        title=data.discription
        titles=generate_Blog_title(title)
        res={"user_prompt":title,"title":titles}
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully generated Blog Titles", "httpStatusCode": status.HTTP_200_OK, "data": res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate Blog Titles", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
@blog_generation_router.post("/brandmind/genrerate-blog")
async def generateBlog(data:BlogContent):
    try:
        companyinfo=None
        title=data.title
        company_id=data.company_id
        brand_id=data.brand_id
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
        structure_generation=generate_Blog_Structure(title,str(companyinfo))
    except Exception as e:
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate Blog", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
    try:
        company_data= companyinfo
        brand_info_summary=None
        marketing_info_summary=None
        company_info_summary=None
        if companyinfo:
            if companyinfo['brandProfile']:
                company_brand_info=companyinfo['brandProfile'][0]
                brand_market_info=companyinfo['brandProfile'][0]['marketInformation']
                del company_data['brandProfile']
                company_info_summary=company_info_summerizer(company_data)
                brand_info_summary=brand_info_summerizer(company_brand_info)
                marketing_info_summary=marketing_info_summerizer(brand_market_info)
    except Exception as e:
        logger.critical(f"Failed to generate summary of company: {e}")
        return JSONResponse(
        content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
        status_code=status.HTTP_404_NOT_FOUND
    )
    try:
        blog_generation=generate_Blog_Content(title,structure_generation,str(companyinfo))
        res={"user_prompt":title,"blog":blog_generation,"companyInfo":company_info_summary,"brandInfo":brand_info_summary,"marketInfo":marketing_info_summary,"companyId":company_id,"brandId":brand_id}
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully generated Blog", "httpStatusCode": status.HTTP_200_OK, "data": res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate Blog", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
    

@blog_generation_router.post("/brandmind/generate-blog-images")
async def generate_blog_images(data:BlogImages):
    title=data.title
    content=data.content
    try:
        multi_image_prompts=blogMultiPromptGenerator(title,content)
        # generated_image=[]
        # image_url_list=[]
        def process_prompt(refined_prompt):
            generated_image = dalle_image_generation(refined_prompt)
            s3_object_name, image_url_multi = upload_base64_image_to_s3(generated_image)
            return s3_object_name, image_url_multi
        with concurrent.futures.ThreadPoolExecutor() as executor:
            results = executor.map(process_prompt, multi_image_prompts)
        image_data = list(results)
        generated_image = [item[0] for item in image_data]
        image_url_list = [item[1] for item in image_data]
        # for prompt in multi_image_prompts:
        #     image=dalle_image_generation(prompt)
        #     s3_object_name,image_url=upload_base64_image_to_s3(image)
        #     image_url_list.append(image_url)
        #     generated_image.append(s3_object_name)
        res={"user_promot":title,"images_object_name":generated_image,"image_url_list":image_url_list}
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully generated Blog Images", "httpStatusCode": status.HTTP_200_OK, "data": res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate Blog Images", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )