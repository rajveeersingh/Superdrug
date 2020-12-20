import traceback
import requests
import re
import json
import time
import threading
from bs4 import BeautifulSoup
from bson import json_util
from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from db import connection



option = Options()
option.headless=True
# driver = webdriver.Firefox(executable_path="/home/superadmin/geckodriver-v0.28.0-linux64/geckodriver")
driver  =  webdriver.Chrome()

headers = {'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:83.0) Gecko/20100101 Firefox/83.0'}
db = connection()

def review_text(code,driver):
            print(code)
            db = connectio
            id = f"sduk_{code}"
            total_review = 0
            try:
                try:
                    reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A{code}&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{code}&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=2&offset.q1=0&limit_comments.q1=3&callback=bv_351_10687'
                    # reviews_text = requests.get(reviews_url, headers=headers).text
                    # print(reviews_text)
                    driver.get(reviews_url)
                    test = driver.page_source
                    soup = BeautifulSoup(test,'html.parser')
                    reviews_text = soup.text
                    # print(soup)
                    reviews = re.search(r'\((.*?)\)$', reviews_text).group(1)
                    reviews = json.loads(str(reviews))
                    total_review = int(reviews['BatchedResults']['q1']['TotalResults'])
                except requests.exceptions.HTTPError as errh:
                    print("Http Error:", errh)
                except requests.exceptions.ConnectionError as errc:
                    print("Error Connecting:", errc)
                except requests.exceptions.Timeout as errt:
                    print("Timeout Error:", errt)
                except requests.exceptions.RequestException as err:
                    print("OOps: Something Else", err)
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print(e)

                review = []
                rev = db.find_one({'_id':id},{'reviews.submissionId':1,'_id':0})
                status = not bool(rev)
                if status:
                    raise KeyError
                rev = rev['reviews']
                revi = ()
                for i in rev:
                    revi = revi+(i['submissionId'],)
                print(revi)

                if bool(total_review):

                    for j in range(0, total_review,100):
                        try:
                            reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A{code}&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{code}&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=100&offset.q1={j}&limit_comments.q1=3&callback=bv_351_10687'
                            # reviews_text = requests.get(reviews_url, headers=headers).text
                            driver.get(reviews_url)
                            test = driver.page_source
                            soup = BeautifulSoup(test, 'html.parser')
                            reviews_text = soup.text
                            reviews = re.search(r'\((.*?)\)$', reviews_text).group(1)
                            reviews = json.loads(str(reviews))
                            try:
                                for i in range(len(reviews['BatchedResults']['q1']['Results'])):
                                    rating = reviews['BatchedResults']['q1']['Results'][i]['Rating']
                                    text = reviews['BatchedResults']['q1']['Results'][i]['ReviewText']
                                    id = reviews['BatchedResults']['q1']['Results'][i]['Id']
                                    if id not in revi:
                                        review.append({'rating':rating,'submissionId':id
                                                      ,'text':text})
                                    else:
                                        # print(id,'exist')
                                        continue

                            except:
                                review.append("No review for the product")

                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:", errh)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:", errc)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:", errt)
                        except requests.exceptions.RequestException as err:
                            print("OOps: Something Else", err)
                        except Exception as e:
                            traceback.print_tb(e.__traceback__)
                            print(e)
            except KeyError as e:
                print("not available",e)
                if bool(total_review):
                    print("adding new reviews")
                    for j in range(0, total_review, 100):
                        try:
                            reviews_url = f'https://api.bazaarvoice.com/data/batch.json?passkey=i5l22ijc8h1i27z39g9iltwo3&apiversion=5.5&displaycode=10798-en_gb&resource.q0=products&filter.q0=id%3Aeq%3A{code}&stats.q0=questions%2Creviews&filteredstats.q0=questions%2Creviews&filter_questions.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_answers.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviews.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q0=contentlocale%3Aeq%3Aen_GB%2Cen_US&resource.q1=reviews&filter.q1=isratingsonly%3Aeq%3Afalse&filter.q1=productid%3Aeq%3A{code}&filter.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&sort.q1=relevancy%3Aa1&stats.q1=reviews&filteredstats.q1=reviews&include.q1=authors%2Cproducts%2Ccomments&filter_reviews.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_reviewcomments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&filter_comments.q1=contentlocale%3Aeq%3Aen_GB%2Cen_US&limit.q1=100&offset.q1={j}&limit_comments.q1=3&callback=bv_351_10687'
                            # reviews_text = requests.get(reviews_url, headers=headers).text
                            driver.get(reviews_url)
                            test = driver.page_source
                            soup = BeautifulSoup(test, 'html.parser')
                            reviews_text = soup.text
                            reviews = re.search(r'\((.*?)\)$', reviews_text).group(1)
                            reviews = json.loads(str(reviews))
                            try:
                                for i in range(len(reviews['BatchedResults']['q1']['Results'])):
                                    rating = reviews['BatchedResults']['q1']['Results'][i]['Rating']
                                    text = reviews['BatchedResults']['q1']['Results'][i]['ReviewText']
                                    id = reviews['BatchedResults']['q1']['Results'][i]['Id']
                                    review.append({'rating': rating, 'submissionId': id
                                                      , 'text': text})
                            except:
                                review.append("No review for the product")
                        except requests.exceptions.HTTPError as errh:
                            print("Http Error:", errh)
                        except requests.exceptions.ConnectionError as errc:
                            print("Error Connecting:", errc)
                        except requests.exceptions.Timeout as errt:
                            print("Timeout Error:", errt)
                        except requests.exceptions.RequestException as err:
                            print("OOps: Something Else", err)
                        except Exception as e:
                            traceback.print_tb(e.__traceback__)
                            print(e)

            except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print(e,'  erroris  ',str(e))
            # print(json.dumps(review,indent=4))
            db = connection()
            if bool(review):
                # print(revi)
                try:
                    print("Updating")
                    db.update({"_id": id}, {"$set": {"reviews": review}})
                    print("Updated")
                except Exception as e:
                    traceback.print_tb(e.__traceback__)
                    print(e)


url = "https://www.superdrug.com/sitemap.xml"
# page = requests.get(url, headers=headers)
driver.get(url)
page = driver.page_source
soup = BeautifulSoup(page, 'html.parser')

code = []
cnt = 0
try:
    for link in soup.findAll('loc'):
        if re.search(r'\/[p]\/[\d]+', link.text):
                    code = str(link.text.split('/')[-1])
                    review_text(code,driver)
                    # code.append(str(link.text.split('/')[-1]))
                    # print(f"sduk_{link.text.split('/')[-1]}")
                    # if len(code)==2:
                    #
                    #     t3 = threading.Thread(target=review_text, args=(code[0],))
                    #     t4 = threading.Thread(target=review_text, args=(code[1],))
                    #     t3.start()
                    #     t4.start()
                    #     code = []
                    # else:
                    #     continue
except Exception as e:
    traceback.print_tb(e.__traceback__)
    print(e)

driver.close()