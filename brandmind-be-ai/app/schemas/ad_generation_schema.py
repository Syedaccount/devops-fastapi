from pydantic import BaseModel
from typing import Dict, Any
class AdGeneration(BaseModel):
    discription:str
    company_id:int
    brand_id:int
    postCreativeId:str
    about_ad:str
    additional_info:str
    additional_keywords:list
    platformId:str
    postCreativeCount:str