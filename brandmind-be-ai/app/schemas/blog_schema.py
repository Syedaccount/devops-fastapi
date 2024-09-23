from pydantic import BaseModel
from typing import Dict, Any
class BlogContent(BaseModel):
    title:str
    company_id:int
    brand_id:int

class BlogTitle(BaseModel):
    discription:str

class BlogImages(BaseModel):
    title:str
    content:str