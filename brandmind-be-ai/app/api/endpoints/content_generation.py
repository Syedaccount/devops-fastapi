from fastapi.responses import JSONResponse
from app.utils.content_generation_utils import generate_Facebook_content,generate_LinkedIn_content,generate_Twitter_content,generate_Instagram_content,generate_tags,TextRefine,company_info_summerizer,marketing_info_summerizer,brand_info_summerizer
from app.utils.utils import remove_emojis
from app.utils.aws_utils import upload_base64_image_to_s3
from app.utils.image_generation_utils import dalle_image_generation,encode_image,image_caption,generate_caption
from app.schemas.content_generation_schema import Content
from fastapi import APIRouter,UploadFile, File,Depends
import logging
from fastapi import status
import requests
import concurrent.futures


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
formatter = logging.Formatter(
    '%(asctime)s:%(name)s:%(levelname)s:%(message)s:%(funcName)s')
file_handler = logging.FileHandler('brand_mind.log')
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)


content_generation_router = APIRouter()
@content_generation_router.post("/brandmind/genrerate-content")
async def generate_content(prompt:Content):
    try:
        # print(file.read())
        caption=None
        companyInfo=None
        generated_image_response=[]
        generated_image_url=[]
        paltformId=prompt.platformId
        postCreativeId=prompt.postCreativeId
        description=prompt.description
        hashtags=prompt.hashtags
        keywords=prompt.keywords
        company_id=prompt.company_id
        brand_id=prompt.brand_id
        image_base64=prompt.image_base64
        if company_id!=0 and brand_id!=0:
            try:
                url = f"https://brandmindbe.xeventechnologies.com/api/companyManagement/getAllCompanyInformation?companyId={company_id}&brandId={brand_id}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                companyInfo=data['data']
            except Exception as e:
                return JSONResponse(content={"succeeded": False, "message": "Company information not retrieved successfully", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND)
        try:
            if paltformId=='101':
                fb_content=generate_Facebook_content(description,str(companyInfo))
                generated_content_response =remove_emojis(fb_content)
                logger.info("Response has been send")
            elif paltformId=='102':
                generated_content_response=generate_LinkedIn_content(description,str(companyInfo))
            elif paltformId=='103':
                generated_content_response=generate_Twitter_content(description,str(companyInfo))
            elif paltformId=='104':
                generated_content_response =generate_Instagram_content(description,str(companyInfo))
        except Exception as e:
            return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
        try:
            if postCreativeId=='111':
                refined_prompt=TextRefine(description,str(companyInfo))
                generated_image=dalle_image_generation(refined_prompt)
                s3_object_name,image_url=upload_base64_image_to_s3(generated_image)
                generated_image_url.append(image_url)
                generated_image_response.append(s3_object_name)
                # generated_image_response = convert_image_url_to_base64(generated_image)
            elif postCreativeId=='113':
                generated_image_response=[]
            elif postCreativeId=='114':
                prompt_list=[]
                for i in range(3):
                    refined_prompt=TextRefine(description,str(companyInfo))
                    prompt_list.append(refined_prompt)
                def process_prompt(refined_prompt):
                    generated_image = dalle_image_generation(refined_prompt)
                    s3_object_name, image_url_multi = upload_base64_image_to_s3(generated_image)
                    return s3_object_name, image_url_multi

                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(process_prompt, prompt_list)
                image_data = list(results)
                generated_image_response = [item[0] for item in image_data]
                generated_image_url = [item[1] for item in image_data]
                #     generated_image=dalle_image_generation(refined_prompt)
                #     s3_object_name,image_url_multi=upload_base64_image_to_s3(generated_image)
                #     generated_image_url.append(image_url_multi)
                #     generated_image_response.append(s3_object_name)
                #     end_time = time.time()
                # execution_time = end_time - start_time
            elif postCreativeId=='115':
                analyze_image_text= image_caption(image_base64)
                caption = generate_caption(analyze_image_text)
        except Exception as ex:
            return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
        try:
            generated_tags=generate_tags(generated_content_response)
            if len(hashtags)!=0:
                generated_tags=generated_tags+hashtags
        except Exception as ex:
            return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )
        try:
            company_data= companyInfo
            brand_info_summary=None
            marketing_info_summary=None
            company_info_summary=None
            if companyInfo:
                if companyInfo['brandProfile']:
                    company_brand_info=companyInfo['brandProfile'][0]
                    brand_market_info=companyInfo['brandProfile'][0]['marketInformation']
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
        res={"user_prompt":description,"description":generated_content_response,"image_object_list":generated_image_response,"image_url_list":generated_image_url,"generatedHashtags":generated_tags,"userHashtags":hashtags,"keywords":keywords,"caption":caption,"companyInfo":company_info_summary,"brandInfo":brand_info_summary,"marketInfo":marketing_info_summary}
        return JSONResponse(
            content={"succeeded": True, "message": "Successfully generated ", "httpStatusCode": status.HTTP_200_OK, "data":res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.critical(f"Failed to generate fb content: {e}")
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )