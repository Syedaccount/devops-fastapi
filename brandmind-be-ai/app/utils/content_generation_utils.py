from langchain_openai import ChatOpenAI
from operator import itemgetter
from langchain_core.prompts import ChatPromptTemplate
import os
from dotenv import load_dotenv

load_dotenv()


def generate_Facebook_content(prompt,companyInfo):
    try:
        prompt_str="""
        You are trained to analyze a topic and generate a Facebook post without containing any (emojis) in the post.
        Analyze the topic and generate a Facebook post. The topic is this: {topic}.
        Follow the instructions:
        1. Response should be in the same language as topic.
        2. If topic is (country) specific, Do not follow the country language,Just follow the overall language of topic.
        3. Shape it like a Facebook Post without containing any kind of (emojis).
        4. Add a catchy opening line (Not more than one line).
        5. Generate text relevant to the topic. (Decide the size of the text depending upon the topic).
        6. Generate the post by keeping in mind the company information.
        7.While generating the post, only use those company information which is relevant or useful for post generation.
        8.Choose the info from company information which is relevant or useful for post generation.
        9. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
        10. It should not generate any harmful text.
        \n
        ((( **company information:** {company_information} )))
       """
        facebook_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher, "company_information":info_fetcher}
        facebook_chain = (setup |facebook_prompt | chat_llm)
        response=facebook_chain.invoke({"topic":prompt,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)
    

def generate_Twitter_content(topic,companyInfo):
    try:
        prompt_str="""
        You are trained to analyze a topic and generate a Twitter post without containing any (emojis) in the post.
        Analyze the topic and generate a twitter post. The topic is this: {topic}.
        Follow the instructions:
        0- Response must not exceed 200 characters.
        1. Response should be in the same language as topic.
        2. If topic is (country) specific, Do not follow the country language,Just follow the overall language of topic.
        3. Shape it like a twitter Post without containing any kind of (emojis).
        4. Add a catchy opening line (Not more than one line).
        5. Generate the post by keeping in mind the company information.
        6.While generating the post, only use those company information which is relevant or useful for post generation.
        7.Choose the info from company information which is relevant or useful for post generation.
        8. Generate text relevant to the topic. (Decide the size of the text depending upon the topic).
        9. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
        10. It should not generate any harmful text.
        \n
        ((( **company information:** {company_information} )))
       """
        twitter_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher,"company_information":info_fetcher}
        twitter_chain = (setup |twitter_prompt | chat_llm)
        response=twitter_chain.invoke({"topic":topic,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)
    


def generate_LinkedIn_content(topic,companyInfo):
    try:
        prompt_str = """
        You are trained to analyze a topic and generate an LinkedIn post.First analyze the (Language) of topic
        Analyze the topic and generate an LinkedIn post without any type of (emojis). The topic is: {topic}.
        Follow the instruction:
        1. Response should be in the same language as the language of topic.
        2. If topic is (country) specific, Do not follow the country language,Just follow the overall language of topic.
        3. Shape it like a LinkedIn Post without containing any kind of (emojis).
        4. Start your post with an engaging and attention-grabbing opening sentence. This should be concise and highlight the main point or message you want to convey.
        5. Generate the post by keeping in mind the company information.
        6.While generating the post, only use those company information which is relevant or useful for post generation.
        7.Choose the info from company information which is relevant or useful for post generation.
        8. Generate text relevent to the topic. (Decide the size of the text depending upon the topic).
        9. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
        10. It should not generate any harmful text.
        \n
        ((( **company information:** {company_information} )))
        """
        

        linkedIn_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher, "company_information":info_fetcher}
        linkedIn_chain = (setup |linkedIn_prompt | chat_llm)
        response=linkedIn_chain.invoke({"topic":topic,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)
    
def generate_Instagram_content(topic,companyInfo):
    try:
        prompt_str = """You are trained to analyze a topic and generate an Instagram caption without adding (emojis) in the caption.
        Analyze the topic and generate an instagram caption without any kind of (emojis). The Topic is: {topic}.
        Follow the instruction:
        1. Response should be in the same language as topic.
        2. If topic is (country) specific, Do not follow the country language,Just follow the overall language of topic.
        3. Shape it like an instagram caption without containing any (emojis).
        4. Add a catchy opening line (Not more than one line, not any emojis).
        5. Generate the post by keeping in mind the company information.
        6. While generating the post, only use those company information which is relevant or useful for post generation.
        7. Choose the info from company information which is relevant or useful for post generation.
        8. Generate text relevant to the topic.
        9. If relevant, you can include hashtags to categorize your post and make it more discoverable but not (emojis).
        10. It should not generate any harmful text.
        \n
        ((( **company information:** {company_information} )))
        """
        instagram_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        info_fetcher= itemgetter("company_information")
        setup={"topic":query_fetcher, "company_information":info_fetcher}
        instagram_chain = (setup |instagram_prompt | chat_llm)
        response=instagram_chain.invoke({"topic":topic,"company_information":companyInfo}).content
        return response
    except Exception as ex:
        return str(ex)




def commentReplier(comment):
    try :
        prompt_str = """You are trained to Analyze the {comment} and generate the (Reply) depending on comment.First analyze a comment (Tone) and (Topic) and generate (Reply) according to comment.Response only contain (Reply) with no heading.Response should be in the same language as comment
        Analyze the comment and generate Reply.The comment is: comment.
        Follow the instruction:
        1. Response should be in the same language as comment
        2. If comment is (Rude) than (reply) should be (neutral).
        3. If comment is (Jolly) than (reply) should be (Jolly). 
        4. If comment is (Neutral) than (reply) should be (Neutral).
        5. If comment is (Appreciation) than reply with ("Thanks").
        6. If you do not understand the comment than reply with ("Thanks for sharing your FeedBack.").
        7. If comment is (greeting) than greet accordingly but do not give any suggestions or assistance.
        8. If comment is a (suggestion) just reply with "We appreciate your suggestion".
        9. If comment is (opinion) Do not agree with it just reply with ("Thanks for Sharing your feedback)".
        10.If comment is (Promotional) just reply with ("Thanks for Sharing your feedback").
        11.If comment  is (Request) just reply with ("I Appreciate Your comment").
        12.If comment is (informative and business-oriented) just reply with (""Thanks for Sharing your feedback").
        13.If comment contain (some key points). Do not Explain it.Just reply with ("I Appreciate Your comment.").
        14.If comment is (Defining) someone or something just reply with "Thank you for sharing your perspective". 
        15.If comment is (instructive) than just reply with "Thanks."
        16. If comment is (Toxic) just reply with "Thank you for sharing your perspective".
        17.If comment is (abusive) just reply with "Thank you for sharing your perspective".
        18.Do not add comment in response.
        19. If comment is containing some personal Insights or sharing than just reply with "Thanks For sharing".
        20. Ananlyze the (Topic) and (Tone) of comment properly.
        21. Reply Should be (Concise) and to the point.
        22. Reply should contain (At most) 20 words.
        23. Response only contain (Reply) with no (heading).
        24. It should not generate any harmful text. """
        
        comment_replier = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("comment")
        setup={"comment":query_fetcher}
        comment_chain = (setup |comment_replier | chat_llm)
        response=comment_chain.invoke({"comment":comment}).content
        return response
    except Exception as ex:
        return str(ex)
  


def generate_Blog_SEO(topic):
    try :
        prompt_str = """You are trained to analyze a {topic} and generate (8) (SEO) keywords of a blog post depending upon the topic.Only generate (SEO) keywords.Response should be in the same language as topic.
        Analyze the topic and generate the (SEO) of a blog post.
        Generate (8) (SEO) keywords for blog post.The (SEO) keywords would varry on the topic.And generate Seo keywords in the form of this '#SEO,#SEO,#SEO'.Only generate (SEO) keywords.Response should be in the same language as topic."""
        generate_blog_seo_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("topic")
        setup={"topic":query_fetcher}
        facebook_chain = (setup |generate_blog_seo_prompt | chat_llm)
        response=facebook_chain.invoke({"topic":topic}).content
        return response
    except Exception as ex:
        return str(ex)

    


def generate_tags(query1):
    try:
        prompt_str="""You are expert in generating Hashtags for specifc post.\n
        ---Analyze the **post** and generate **6** hashtags. \n
        ---Response must be in the list format.\n
        ---Example of valid response:
            hashtag, hashtag, hashtag, hashtag, hashtag, hashtag
        End of valid response example.
        \n
        **post:** {tags}
       """
        hashtag_prompt = ChatPromptTemplate.from_template(prompt_str)
        chat_llm = ChatOpenAI(model='gpt-4o-mini',openai_api_key=os.getenv("OPENAI_API_KEY"),temperature=0)
        query_fetcher= itemgetter("tags")
        setup={"tags":query_fetcher}
        hashtag_chain = (setup |hashtag_prompt | chat_llm)
        response=hashtag_chain.invoke({"tags":query1}).content.split(",")
        return response
    except Exception as ex:
        return str(ex)
    




def TextRefine(query,companyInfo):
    try:
        prompt_str="""Write a prompt that can generate the Stunning, realistic, high quality 4k photography and showcasing the beauty images based on the topic.
        --Portray every detail of topic with stunning realism.
        --The prompt should clearly define the image content and mention the quality of image.
        --The prompt should be less than 30 words.
        --While generating the prompt, keep the company information as a context.
        --Use only those information from company information which is useful for generating prompt.
        \n
        topic: {topic}

        (((**company information:** {company_information} )))

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



def company_info_summerizer(companyInfo):
    try:
        template = """You are an expert AI Summuraizer specilized in Company information summerizing.
        Your task is to summerize the company information provided by the user.
        Company Information: {companyInfo}
        Instructions:
        **1. Analyze the Company information properly.**
        **2. Summerize the company information in 3 to 4 lines.**
        **3. Do not exceed to 4 lines.**
        """
        prompt = ChatPromptTemplate.from_template(template)
        model = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
        chain =prompt | model 
        res = chain.invoke({"companyInfo": companyInfo}).content
        return res
    except Exception as e:
        raise e

def brand_info_summerizer(brandInfo):
    try:
        template = """You are an expert AI Summuraizer specilized in Comapany's Brand information summerizing.
        Your task is to summerize the Brand's information provided by the user.
        Comapany's Brand information: {brandInfo}
        Instructions:
        **1. Analyze the Comapany's Brand information properly.**
        **2. Summerize the Comapany's Brand information in 3 to 4 lines.**
        **3. Do not exceed to 4 lines.**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model 
        res = chain.invoke({"brandInfo": brandInfo}).content
        return res
    except Exception as e:
        raise e


def marketing_info_summerizer(marketInfo):
    try:
        template = """You are an expert AI Summuraizer specilized in Marketing information of company's brand summerizing.
        Your task is to summerize the Marketing information of company's brand provided by the user.
        Marketing information of company's brand: {marketInfo}
        Instructions:
        **1. Analyze the Marketing information of company's brand properly.**
        **2. Summerize the Marketing information of company's brand in 3 to 4 lines.**
        **3. Do not exceed to 4 lines.**
        """
        model = ChatOpenAI(model="gpt-4o-mini",api_key=os.getenv("OPENAI_API_KEY"))
        prompt = ChatPromptTemplate.from_template(template)
        chain = prompt | model
        res = chain.invoke({"marketInfo": marketInfo}).content
        return res
    except Exception as e:
        raise e