
from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv
load_dotenv()



def generate_Blog_Structure(titile,companyinfo):
    try:
        prompt_str="""
        You are trained to analyze a title and generate the structure of a blog post depending upon the Title.First analyze the (Language) of title and responsed must be in same language as the language of title. \n
        Follow these instructions:
        1-If title is (country) specific, Do not follow the country language,Just follow the overall language of title.
        2-Generate a structure to help generate a blog post on that.
        3-Structure must contain (Reference) Heading. 
        4-The structure would varry on the Title.
        5. Generate the structure by keeping in mind the company information.
        6. While generating the structure, only use those company information which is relevant or useful for structure generation.
        7. Choose the info from company information which is relevant or useful for structure generation.
        \n
        (((title: {title} )))
        \n
        ((( companyinfo: {companyinfo} )))

       """
        blog_structure_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        title_fetcher= itemgetter("title")
        info_fetcher= itemgetter("companyinfo")
        setup={"title":title_fetcher, "companyinfo":info_fetcher}
        blog_strucure_chain = (setup |blog_structure_prompt | chat_llm)
        response=blog_strucure_chain.invoke({"title":titile,"companyinfo":companyinfo}).content
        return response
    except Exception as ex:
        return str(ex)
    

def generate_Blog_Content(title, structure,companyinfo):
    try:
        prompt_str="""
        You are trained to analyze a title and structure to generate a blog post, depending on the given structure.\n
        Follow these instructions:
        1-First analyze the (Language) of title and structure and responsed must be in same language.
        2-If title and structure is (country) specific, Do not follow the country language,Just follow the overall language of title and structure.
        3- Response should be in the same language as title and structure.
        5. You must not add "Title" in the Blog post.
        5- Add authentic (HTTP links) in (Reference) heading of Blog post.
        6- Blog post must contain 3000 to 4000 words.
        7. Generate the Blog by keeping in mind the company information.
        8. While generating the Blog, only use those company information which is relevant or useful for Blog generation.
        9. Choose the info from company information which is relevant or useful for Blog generation.
        \n
        ((( title: {title}  ))) \n
        ((( structure: {structure}))) \n
        ((( companyinfo: {companyinfo} )))
       """
        blog_generation_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        title_fetcher= itemgetter("title")
        structure_fetcher= itemgetter("structure")
        info_fetcher= itemgetter("companyinfo")
        setup={"title":title_fetcher, "companyinfo":info_fetcher,"structure":structure_fetcher}
        blog_generation_chain = (setup |blog_generation_prompt | chat_llm)
        response=blog_generation_chain.invoke({"title":title,"structure":structure,"companyinfo":companyinfo}).content
        return response.replace("#","").strip()
    except Exception as ex:
        return str(ex)
    

def generate_Blog_title(topic):
    try:
        prompt_str="""
        You are trained to analyze a topic and generate (5) (Titles) of a blog post depending upon the topic. 
        -Get the idea from topic of (blog) and write (5) (Titles).
        -The Titles should be relevant to topic.
        -As we need 5 Title in return.So,response must be like this: ((Title1\n\n Title2 \n\n Title3 \n\n Title4 \n\n Title5)).
        -Response must be in the same language as topic.
        \n
        (((topic: {topic} )))
       """
        title_generation_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        topic_fetcher= itemgetter("topic")
        setup={ "topic":topic_fetcher}
        title_generation_chain = (setup |title_generation_prompt | chat_llm)
        response=title_generation_chain.invoke({"topic":topic}).content
        response=response.replace("(","").replace(")","")
        response=response.split("\n\n")
        return response
    except Exception as ex:
        return str(ex)