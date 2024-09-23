from langchain.utilities import SerpAPIWrapper
from dotenv import load_dotenv
import os
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI


load_dotenv()

OPENAI_API_KEY=os.getenv('OPENAI_API_KEY')


def trendFetcher(topic):
    search = SerpAPIWrapper(serpapi_api_key=os.getenv("SERP_API_KEY"))
    final_query=f"Give me latest trend on this topic: {topic}"
    result = search.run(final_query)
    return result



def facebook_trend_prompt(trends):
    try:
        template = """You are expert prompt generation for llm. Generate a prompt regarding the trends {trends}
        that would pass to another llm to generate content about the trends for facebook post generation.
        Instructions:
        **1. Genreate maximum 2 lines of prompt.**
        **2. Always start with "Generate a Facebook post" because other llm use this prompt for Facebook post generation.**
        **3. Generate only a sinlge prompt by summerizing the trends and thier descriptions**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser
        res = chain.invoke({"trends": trends})
        return res
    except Exception as e:
        raise e

def instagram_trend_prompt(trends):
    try:
        template = """You are expert prompt generation for llm. Generate a prompt regarding the trends {trends}
        that would pass to another llm to generate content about the trends for instagram post generation.
        Instructions:
        **1. Genreate maximum 2 lines of prompt.**
        **2. Always start with "Generate a instagram post" because other llm use this prompt for instagram post generation.**
        **3. Generate only a sinlge prompt by summerizing the trends and thier descriptions**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser
        res = chain.invoke({"trends": trends})
        return res
    except Exception as e:
        raise e

def twitter_trend_prompt(trends):
    try:
        template = """You are expert prompt generation for llm. Generate a prompt regarding the trends {trends}
        that would pass to another llm to generate content about the trends for twitter post generation.
        Instructions:
        **1. Genreate maximum 2 lines of prompt.**
        **2. Always start with "Generate a twitter post" because other llm use this prompt for twitter post generation.**
        **3. Generate only a sinlge prompt by summerizing the trends and thier descriptions**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser
        res = chain.invoke({"trends": trends})
        return res
    except Exception as e:
        raise e
    

    
def linkedin_trend_prompt(trends):
    try:
        template = """You are expert prompt generation for llm. Generate a prompt regarding the trends {trends}
        that would pass to another llm to generate content about the trends for linkedin post generation.
        Instructions:
        **1. Genreate maximum 2 lines of prompt.**
        **2. Always start with "Generate a linkedin post" because other llm use this prompt for linkedin post generation.**
        **3. Generate only a sinlge prompt by summerizing the trends and thier descriptions**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=OPENAI_API_KEY)
        prompt = ChatPromptTemplate.from_template(template)
        output_parser = StrOutputParser()
        chain = prompt | model | output_parser
        res = chain.invoke({"trends": trends})
        return res
    except Exception as e:
        raise e