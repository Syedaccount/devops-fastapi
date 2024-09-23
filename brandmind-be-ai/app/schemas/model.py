from pydantic import BaseModel

class BlogGeneration(BaseModel):
    blog_prompt : str

class Image_prompt_generate(BaseModel):
    topic:str
    content:str

class Generate_Blog_Seo(BaseModel):
    prompt:str

class Generate_comment_reply(BaseModel):
    comment : str

class Instagram_Generation(BaseModel):
    instagram_prompt:str

class Twitter_Generation(BaseModel):
    twitter_prompt:str

class Facebook_Generation(BaseModel):
    facebook_prompt:str

class Linkedin_Generation(BaseModel):
    linkedin_prompt:str

class Refined_Prompt(BaseModel):
    description:str

class Content(BaseModel):
    platformId:str
    postCreativeId:str
    description:str
    hashtags:list
    keywords:list
