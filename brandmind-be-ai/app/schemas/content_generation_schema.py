
from pydantic import BaseModel,Json
from typing import List,Dict, Any
class Content(BaseModel):
    platformId:str
    postCreativeId:str
    description:str
    hashtags:List[str]
    keywords:List[str]
    company_id:int
    brand_id:int
    image_base64:str