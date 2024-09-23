from pydantic import BaseModel


class AutoGeneration(BaseModel):
    companyId:int
    brandId:int
    platformId:str