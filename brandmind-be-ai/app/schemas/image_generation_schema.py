from pydantic import BaseModel
from typing import Dict, Any


class Refined_Prompt(BaseModel):
    description:str
    company_id:int
    brand_id:int