from fastapi.responses import JSONResponse
from app.utils.content_generation_utils import generate_Facebook_content,generate_LinkedIn_content,generate_Twitter_content,generate_Instagram_content,generate_tags,TextRefine,company_info_summerizer,marketing_info_summerizer,brand_info_summerizer
from app.utils.utils import remove_emojis
from app.utils.aws_utils import upload_base64_image_to_s3
from app.utils.image_generation_utils import dalle_image_generation,encode_image,image_caption,generate_caption
from app.utils.auto_generation_utils import trendFetcher,facebook_trend_prompt,instagram_trend_prompt,linkedin_trend_prompt,twitter_trend_prompt
from app.schemas.auto_content_generation_schema import AutoGeneration
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


aut_content_generation_router = APIRouter()


@aut_content_generation_router.post("/brandmind/auto-content-generation")
async def generate_auto_content(prompt:AutoGeneration):
    try:
        # print(file.read())
        description=None
        companyInfo=None
        generated_image_response=[]
        generated_image_url=[]
        company_id=prompt.companyId
        brand_id=prompt.brandId
        paltformId=prompt.platformId
        if company_id!=0 and brand_id!=0:
            try:
                url = f"https://brandmindbe.xeventechnologies.com/api/companyManagement/getAllCompanyInformation?companyId={company_id}&brandId={brand_id}"
                response = requests.get(url)
                response.raise_for_status()
                data = response.json()
                companyInfo=data['data']
                company_business_type=data['data']['brandProfile'][0]['businessType']
            except Exception as e:
                return JSONResponse(content={"succeeded": False, "message": "Company information not retrieved successfully", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND)
        if companyInfo:
            try:
                recent_trends=trendFetcher(company_business_type)
            except Exception as e:
                return JSONResponse(content={"succeeded": False, "message": "Failed to fetch recent trends", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND)
            try:
                if paltformId=='101':
                    description=facebook_trend_prompt(recent_trends)
                    fb_content=generate_Facebook_content(description,str(companyInfo))
                    generated_content_response =remove_emojis(fb_content)
                    logger.info("Response has been send")
                elif paltformId=='102':
                    description=linkedin_trend_prompt(recent_trends)
                    generated_content_response=generate_LinkedIn_content(description,str(companyInfo))
                elif paltformId=='103':
                    description=twitter_trend_prompt(recent_trends)
                    generated_content_response=generate_Twitter_content(description,str(companyInfo))
                elif paltformId=='104':
                    description=instagram_trend_prompt(recent_trends)
                    generated_content_response =generate_Instagram_content(description,str(companyInfo))
            except Exception as e:
                return JSONResponse(
                content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND
            )
            try:
                refined_prompt=TextRefine(description,str(companyInfo))
                generated_image=dalle_image_generation(refined_prompt)
                s3_object_name,image_url=upload_base64_image_to_s3(generated_image)
                generated_image_url.append(image_url)
                generated_image_response.append(s3_object_name)
                # generated_image_response = convert_image_url_to_base64(generated_image)

            except Exception as ex:
                return JSONResponse(
                content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND
            )
            try:
                generated_tags=generate_tags(generated_content_response)
            except Exception as ex:
                return JSONResponse(
                content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
                status_code=status.HTTP_404_NOT_FOUND
            )
            res={"user_prompt":description,"image_object_list":generated_image_response,"image_url_list":generated_image_url,"generatedHashtags":generated_tags,"generatedPost":generated_content_response}
            return JSONResponse(
                content={"succeeded": True, "message": "Successfully generated ", "httpStatusCode": status.HTTP_200_OK, "data":res},
                status_code=status.HTTP_200_OK
            )
        else:
            return JSONResponse(
                content={"succeeded": True, "message": "Company information not found", "httpStatusCode": status.HTTP_200_OK},
                status_code=status.HTTP_200_OK
            )
    except Exception as e:
        logger.critical(f"Failed to generate fb content: {e}")
        return JSONResponse(
            content={"succeeded": False, "message": "Unsuccesfull to generate content", "httpStatusCode": status.HTTP_404_NOT_FOUND},
            status_code=status.HTTP_404_NOT_FOUND
        )