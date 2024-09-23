from fastapi.responses import JSONResponse
from app.utils.ad_generation_utils import TextRefineAdFb,TextRefineAdInsta
from app.utils.image_generation_utils import dalle_image_generation
from app.utils.content_generation_utils import marketing_info_summerizer,brand_info_summerizer,company_info_summerizer
from app.utils.aws_utils import upload_base64_image_to_s3
from app.schemas.ad_generation_schema import AdGeneration
from fastapi import APIRouter
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


ad_generation_router = APIRouter()

@ad_generation_router.post("/brandmind/generate-ad")
async def generate_ad(ad_generation: AdGeneration):
    try:
        companyinfo=None
        generated_image_url=[]
        generated_iamges_object=[]
        discription=ad_generation.discription
        company_id=ad_generation.company_id
        brand_id=ad_generation.brand_id
        postCreativeId=ad_generation.postCreativeId
        about_ad=ad_generation.about_ad
        additional_info=ad_generation.additional_info
        additional_keywords=ad_generation.additional_keywords
        postCreativeCount=ad_generation.postCreativeCount
        platformId=ad_generation.platformId
        if postCreativeCount=='0':
            return JSONResponse(
                content={"succeeded": True, "message": "Count must be equal or greater than 1", "httpStatusCode": status.HTTP_200_OK},
                status_code=status.HTTP_200_OK
            )
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
        final_query=f"discription: {discription} \n 'Ad should be like this:' {about_ad} \n 'additional_info:' {additional_info}"
        def generate_single_ad(refined_prompt):
            """Helper function to generate and upload image from a refined prompt."""
            generated_image = dalle_image_generation(refined_prompt)
            return upload_base64_image_to_s3(generated_image)
        if platformId == "101":
            if postCreativeId=='111':
                prompt_list = [TextRefineAdFb(final_query, str(companyinfo)) for _ in range(int(postCreativeCount))]
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(generate_single_ad, prompt_list)
                
                for result in results:
                    s3_object_name, image_url = result
                    generated_image_url.append(image_url)
                    generated_iamges_object.append(s3_object_name)
            elif postCreativeId=='114':
                total_images_to_generate = int(postCreativeCount) * 3  # 3 images per count
                prompt_list = [TextRefineAdFb(final_query, str(companyinfo)) for _ in range(total_images_to_generate)]

                # Concurrent image generation
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(generate_single_ad, prompt_list)
                
                # Collect generated images and URLs
                image_data = list(results)
                generated_iamges_object = [{"s3_objects": [item[0] for item in image_data[i:i + 3]]}  # object names
                                          for i in range(0, len(image_data), 3) ]
                generated_image_url = [
                    {"urls": [item[1] for item in image_data[i:i + 3]]}  # image URLs
                    for i in range(0, len(image_data), 3)
                ]
        elif platformId=="104":
            if postCreativeId=='111':
                prompt_list = [TextRefineAdInsta(final_query, str(companyinfo)) for _ in range(int(postCreativeCount))]
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(generate_single_ad, prompt_list)
                
                for result in results:
                    s3_object_name, image_url = result
                    generated_image_url.append(image_url)
                    generated_iamges_object.append(s3_object_name)
            elif postCreativeId=='114':
                total_images_to_generate = int(postCreativeCount) * 3  # 3 images per count
                prompt_list = [TextRefineAdInsta(final_query, str(companyinfo)) for _ in range(total_images_to_generate)]

                # Concurrent image generation
                with concurrent.futures.ThreadPoolExecutor() as executor:
                    results = executor.map(generate_single_ad, prompt_list)
                
                # Collect generated images and URLs
                image_data = list(results)
                generated_iamges_object = [{"s3_objects": [item[0] for item in image_data[i:i + 3]]}  # object names
                                          for i in range(0, len(image_data), 3) ]
                generated_image_url = [
                    {"urls": [item[1] for item in image_data[i:i + 3]]}  # image URLs
                    for i in range(0, len(image_data), 3)
                ]
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
        res={"user_prompt":discription,"iamge_object_name":generated_iamges_object, "image_url":generated_image_url,"companyInfo":company_info_summary,"brandInfo":brand_info_summary,"marketInfo":marketing_info_summary,"Additional_keywords":additional_keywords,"company_id":company_id,"brand_id":brand_id,"platformId":platformId,"postCreativeCount":postCreativeCount}
        return JSONResponse(
            content={"succeeded": True, "message": "Ad generated successfully", "httpStatusCode": status.HTTP_200_OK, "data": res},
            status_code=status.HTTP_200_OK
        )
    except Exception as e:
        logger.error(f"Error in generating ad: {e}")
        return JSONResponse(
            content={"succeeded": False, "message": "Error in generating ad", "httpStatusCode": status.HTTP_500_INTERNAL_SERVER_ERROR},
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
