from lxml import html
from json import dump,loads
from requests import get
import json
from re import sub
from dateutil import parser as dateparser
from time import sleep
import requests


def ParseReviews(asin):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36'}
    reviews_list = []
    for j in range(1,5):
        
        if j==1:
            amazon_url  = 'http://www.amazon.in/dp/'+ asin
        else:   
            
            amazon_url = 'https://www.amazon.in/product-reviews/'+ asin + '?pageNumber=' + str(j)    
    
        response = get(amazon_url, headers = headers, verify=False, timeout=30)
        if response.status_code == 404:
            return {"url": amazon_url, "error": "page not found"}
        if response.status_code != 200:
            continue
        
        cleaned_response = response.text.replace('\x00', '')
        
        parser = html.fromstring(cleaned_response)
        XPATH_AGGREGATE = '//span[@id="acrCustomerReviewText"]'
        XPATH_REVIEW_SECTION_1 = '//div[contains(@id,"reviews-summary")]'
        XPATH_REVIEW_SECTION_2 = '//div[@data-hook="review"]'
        XPATH_AGGREGATE_RATING = '//table[@id="histogramTable"]//tr'
        
        reviews = parser.xpath(XPATH_REVIEW_SECTION_1)

        
        if not reviews:
            reviews = parser.xpath(XPATH_REVIEW_SECTION_2)
        
        



        for review in reviews:
            XPATH_RATING  = './/i[@data-hook="review-star-rating"]//text()'
            
            XPATH_REVIEW_POSTED_DATE = './/span[@data-hook="review-date"]//text()'
            XPATH_REVIEW_TEXT_1 = './/div[@data-hook="review-collapsed"]//text()'
            XPATH_REVIEW_TEXT_3 = './/span[@data-hook="review-body"]//text()'
            XPATH_REVIEW_COMMENTS = './/span[@data-hook="review-comment"]//text()'
            
            XPATH_REVIEW_TEXT_2 = './/div[@data-hook="customer_review"]//text()'
            #XPATH_REVIEW_TEXT_3 = './/div[contains(@id,"dpReviews")]/div/text()'
            
            
            raw_review_rating = review.xpath(XPATH_RATING)
            
            raw_review_posted_date = review.xpath(XPATH_REVIEW_POSTED_DATE)
            raw_review_text1 = review.xpath(XPATH_REVIEW_TEXT_1)
            raw_review_text2 = review.xpath(XPATH_REVIEW_TEXT_2)
            raw_review_text3 = review.xpath(XPATH_REVIEW_TEXT_3)

            # Cleaning data
            
            review_rating = ''.join(raw_review_rating).replace('out of 5 stars', '')
            

            try:
                review_posted_date = dateparser.parse(''.join(raw_review_posted_date)).strftime('%d %b %Y')
            except:
                review_posted_date = None
            
            if j==1:
            	review_text = ' '.join(raw_review_text1)

            
            	if raw_review_text2:
                	json_loaded_review_data = loads(raw_review_text2[0])
                	json_loaded_review_data_text = json_loaded_review_data['rest']
                	cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
                	full_review_text = review_text+cleaned_json_loaded_review_data_text
            	else:
                	full_review_text = review_text
            else:
                review_text = ' '.join(raw_review_text3)
                if raw_review_text2:
                	json_loaded_review_data = loads(raw_review_text2[0])
                	json_loaded_review_data_text = json_loaded_review_data['rest']
                	cleaned_json_loaded_review_data_text = re.sub('<.*?>', '', json_loaded_review_data_text)
                	full_review_text = review_text+cleaned_json_loaded_review_data_text
                else:
                	full_review_text = review_text
            
           
           
            review_dict = {
                                
                                'review_text': full_review_text.split(),
                                'review_posted_date': review_posted_date,
                                'review_rating': review_rating,
                                

                            }
            reviews_list.append(review_dict)

        
    return reviews_list

        #return {"error": "failed to process the page", "url": amazon_url}
            

def ReadAsin(asin):
    # Add your own ASINs here
    #AsinList = ['B07G7Z51VB']
    extracted_data = []
    f = open('data.json', 'w')

    #for asin in AsinList:
    print("Downloading and processing page http://www.amazon.in/dp/" + asin)
    extracted_data=ParseReviews(asin)
    
    sleep(5)
    dump(extracted_data, f, indent=4)
    print("DONE")
    f.close()


