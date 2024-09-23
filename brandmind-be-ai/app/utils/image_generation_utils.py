import openai
import os
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()
import base64
from fastapi import FastAPI, UploadFile
from PIL import Image
from io import BytesIO
client = OpenAI()
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
import requests
openapi_key = os.getenv("OPENAI_API_KEY")
openai.api_key = openapi_key

def dalle_image_generation(prompt):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024",
    quality="hd",
    n=1,
    )
    image_url = response.data[0].url
    response = requests.get(image_url)
    base64_image = base64.b64encode(response.content).decode('utf-8')
    return base64_image

def encode_image(upload_file: UploadFile):
    image = Image.open(upload_file.file)
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode("utf-8")


def image_caption(image_path):
        response = client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "describe this image?"},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": "data:image/jpeg;base64," + image_path,  # Correctly format the base64 image
                                    },
                                },
                            ],
                        }
                    ],
                    max_tokens=300,
                )
        description = response.choices[0].message.content
        return description


def generate_caption(prompt):
    try:
        prompt_str="""
        As an expert in image analysis and captioning, your task is to create a 
        concise and engaging caption for the following analyzed image description: {analyze_image_text}.
        The caption should be well-crafted, capturing the essence of the image in no 
        more than 2 to 3 lines. Ensure that the caption is clear, relevant, and provides
        an accurate representation of the visual content.
        """
        caption_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("analyze_image_text")
        setup={"analyze_image_text":query_fetcher}
        caption_chain = (setup |caption_prompt | chat_llm)
        response=caption_chain.invoke({"analyze_image_text":prompt}).content
        return response
    except Exception as ex:
        return str(ex)
    



def blogMultiPromptGenerator(title, content):
    try:
        prompt_str="""
        Your role is to generate 3 prompts that can generate stunning, realistic and high qulaity 4k images for (blog). Get the idea from title and content of (blog) and write prompts in atmost 30 words. 
        Follow these instructions:
        1-The prompts should be relevant to title and content.
        2-prompt should focus on a distinct point and contribute to a cohesive set of images for (blog)'s multi-point structure.
        3-the response must not be empty like [''].
        4-As we need 3 prompt in return.So, response must be like this: ((prompt1\n\n prompt2 \n\n prompt3)).

        ((( title: {title}  ))) \n
        ((( content: {content})))
       """
        blog_image_generation_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        title_fetcher= itemgetter("title")
        content_fetcher= itemgetter("content")
        setup={"content":content_fetcher, "title":title_fetcher}
        blog_image_generation_chain = (setup |blog_image_generation_prompt | chat_llm)
        response=blog_image_generation_chain.invoke({"title":title,"content":content}).content
        response=response.replace("(","").replace(")","")
        response=response.split("\n\n")
        return response
    except Exception as ex:
        return str(ex)