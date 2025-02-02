from utils import crawl_website, structured_extract, WebsiteDetail, FBLikes, google_rating_reviews
from urllib.parse import urlparse
import json
import os

from dotenv import load_dotenv
load_dotenv()


def main (url: str):
    webiste_name = url
    crawl_text = crawl_website(webiste_name, limit=2)
    data = structured_extract(crawl_text, method=WebsiteDetail)

    try:
        FacbookPage = data['social_media_profiles'][0]['facebook']
    except: 
        FacbookPage = ''
    if  FacbookPage.startswith('https://'):
        try:
            crawl_fb_text = crawl_website(FacbookPage, limit=1)
            fb_likes = structured_extract(crawl_fb_text, method=FBLikes)
        except:
            fb_likes = None
            pass
    else:
        fb_likes = None
        print("The website doesn't have Facebook Page")


    company_name = data['institute_name']
    places_results = google_rating_reviews(company_name, os.environ['SERP_API_KEY'] ).json()

    if "place_results" in places_results.keys():
        rating = places_results['place_results'].get('rating')
        reviews = places_results['place_results'].get('reviews')
    else:
        rating = None
        reviews = None
        print('The company is not found')

    print(f'{company_name} Average Google Ratings : {rating}')
    print(f'{company_name} Total Reviews : {reviews}')

    data['additional'] = {"FaceBook Likes": fb_likes,
                      'Google Ratings': rating,
                      'Reviews': reviews
                      }
    

    # parsed_url = urlparse(webiste_name)
    # name = parsed_url.netloc.split('.')[0]

    # with open(f'data/{name}.json', 'w') as file:
    #     json.dump(data, file, indent=4)

    return data
