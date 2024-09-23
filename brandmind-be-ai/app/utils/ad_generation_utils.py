from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()






def TextRefineAdFb(query,companyInfo):
    try:
        prompt_str="""Write a prompt that can generate the Stunning, realistic, high quality 4k Facebook Ad and showcasing the beauty images based on the topic.
        --Portray every detail of topic with stunning realism.
        --The prompt should clearly define the Facebook Ad content and mention the quality of Ad.
        --The prompt should be less than 30 words.
        --While generating the prompt, keep the company information as a context.
        --Use only those information from company information which is useful for generating prompt.
        \n
        topic: {topic}

        (((*company information:* {company_information} )))

       """
        text_refine_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher, "company_information":info_fetcher}
        text_refine_chain = (setup |text_refine_prompt | chat_llm)
        response=text_refine_chain.invoke({"topic":query,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)
    

def TextRefineAdInsta(query,companyInfo):
    try:
        prompt_str="""Write a prompt that can generate the Stunning, realistic, high quality 4k Instagram Ad and showcasing the beauty images based on the topic.
        --Portray every detail of topic with stunning realism.
        --The prompt should clearly define the Instagram Ad content and mention the quality of Ad.
        --The prompt should be less than 30 words.
        --While generating the prompt, keep the company information as a context.
        --Use only those information from company information which is useful for generating prompt.
        \n
        topic: {topic}

        (((*company information:* {company_information} )))

       """
        text_refine_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher, "company_information":info_fetcher}
        text_refine_chain = (setup |text_refine_prompt | chat_llm)
        response=text_refine_chain.invoke({"topic":query,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)