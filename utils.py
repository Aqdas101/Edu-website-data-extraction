from openai import OpenAI
from pydantic import BaseModel, Field
from typing import List
from firecrawl import FirecrawlApp
import json
from pydantic import BaseModel, Field
from typing import List, Type, Union
import requests
import os
from dotenv import load_dotenv
load_dotenv()


def crawl_website(website_name: str, limit: int):
    app = FirecrawlApp(api_key=os.environ["FIRE_CRAWL_API"])
    crawl_status = app.crawl_url(
    website_name, 
    params={
        'limit': limit, 
        'scrapeOptions': {'formats': ['markdown', 'html']}
    },
    poll_interval=30
    )

    texts = []

    website_page_markdowns: list = crawl_status['data']
    for data in website_page_markdowns:
        texts.append(data['markdown'])

    crawl_web_text = ''.join(texts)

    return crawl_web_text



def google_rating_reviews(organization: str, api_key):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_maps",  
        "q": f"{organization}", 
        "hl": "en",  
        "gl": "us",  
        "api_key": api_key 
    }
    response = requests.get(url, params=params)

    return response


class Locations(BaseModel):
    num_of_campuses: int = Field(None, description='How many campuses they have')
    main_office_address: str = Field(None, description='The address of their main office')

class SocialMediaLinks(BaseModel):
    linkedin: str = Field(None, description='The linkedin URL of the company If available else None')
    twitter: str = Field(None, description='The twitter URL of the if available else None')
    instagram: str = Field(None, description='The instagram URL of the company if available else None')
    facebook: str = Field(None, description='The facebook URL of the company if available else None')

class CourseDetails(BaseModel):
    course_title: str = Field(None, description='The title of the Only Top Main Major Course')
    sub_skills: str = Field(None, description='What microskills is in this course')
    course_description: str = Field(None, description='The description of the 1st Main course')
    trainin_type: str = Field(None, description="Does the training Provide online or Onsite? If provivded else None")
    course_category: str = Field(None, description='The category of the course')


    
class WebsiteDetail(BaseModel):
    
    institute_name: str = Field(None, description="The name of the institute")
    about_institute: str = Field(None, description="More Information about Institute")
    LOGO_URL: str = Field(None, description='Logo URL IF available else return None')

    contact_number: list[str] = Field(None, description='Contact number or Phone Number if provided else return None')
    institute_website: str = Field(None, description="The website URL of the institute")
    email: list[str] = Field(None, description='info@ email address')

    location: List[Locations] 
    social_media_profiles: List[SocialMediaLinks]
    course_details: List[CourseDetails]

class FBLikes(BaseModel):
    PageLikes: int = Field(None, description='The Pages likes')


# indicates that the method parameter should accept either the FBLikes class or the WebsiteDetail class, but not any other type.

def structured_extract(text: str, method: Type[Union[FBLikes, WebsiteDetail]] ) -> dict:
    client = OpenAI()
    messages = [
      {"role": "system", "content": "Extract the detail from the markdown text"},
      {"role": "user", "content": text},
    ]
    
    response = client.beta.chat.completions.parse(
    model="gpt-4o-2024-08-06",
    messages = messages,
    response_format=method,
    )

    return_json = json.loads(response.choices[0].message.content)

    return return_json






