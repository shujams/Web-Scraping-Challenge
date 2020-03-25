import os
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import re
import time
import datetime as dt
from selenium import webdriver


def mars_news(browser):
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)

    # Get first list item and wait half a second if not immediately present
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=0.5)

    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    try:
        slide_elem = news_soup.select_one("ul.item_list li.slide")
        news_title = slide_elem.find("div", class_="content_title").get_text()
        news_p = slide_elem.find("div", class_="article_teaser_body").get_text()
    except AttributeError:
        return None, None

    browser.quit()
    return news_title, news_p

def featured_image(driver):
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # create a new Chrome session
    driver = webdriver.Chrome()
    #driver.implicitly_wait(6)
    driver.get(url)
    driver.implicitly_wait(6)
    #browser.visit(url)

    #After opening the url above, Selenium clicks the specific agency link
    python_button = driver.find_element_by_id('full_image') #FHSU
    python_button.click() #click fhsu link

    driver.implicitly_wait(7)
    try:
        img_url = driver.find_element_by_xpath('//*[@id="fancybox-lock"]/div/div[1]/img').get_attribute("src")
    except AttributeError:
       return None #print(img_url)
        
    driver.quit()

    return img_url

def hemisphere(browser):
    
    executable_path = { "executable_path" : "chromedriver.exe" }
    browser = Browser('chrome', **executable_path, headless=False)
    url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url)
    hemisphere_image_urls = []
    links = browser.find_by_css("a.product-item h3")

    for i in range(len(links)):
        hemisphere = {}
        
        browser.find_by_css("a.product-item h3")[i].click()
        sample_elem = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = sample_elem['href']
        hemisphere['title'] = browser.find_by_css('h2.title').text
        
        hemisphere_image_urls.append(hemisphere)
        browser.back()

    browser.quit()    
    return hemisphere_image_urls

def twitter_weather(browser):
    
    url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url)
    time.sleep(7)

    html = browser.html
    weather_soup = BeautifulSoup(html, 'html.parser')

    mars_weather_tweet = weather_soup.find('div', attrs={'class' :'tweets', 'data-name' : 'Mars Weather'})
    print(mars_weather_tweet) # findind the first tweet

    try:
        mars_weather = mars_weather_tweet.find('p', 'tweet-text').get_text()
        print(mars_weather) # finding the weather

    except AttributeError:
        pattern = re.compile(r'sol')
        mars_weather = weather_soup.find("span", text=pattern).text
    
    browser.quit()
    return mars_weather


def mars_facts():
    
    try:
        mars_facts_df = pd.read_html("https://space-facts.com/mars/")[0]
    except BaseException:
        return None

    mars_facts_df.columns = ["description", "value"]
    mars_facts_df.set_index("description", inplace=True)

    return mars_facts_df.to_html(classes="table table-striped")

def scrape_all():
    executable_path = { "executable_path" : "chromedriver.exe" }
    browser = Browser("chrome", executable_path="chromedriver.exe", headless=False)
    driver = webdriver.Chrome()

    news_title, news_paragraph = mars_news(browser)

    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "facts": mars_facts(),
        "featured_image": featured_image(driver),
        "weather" : twitter_weather(browser),
        "hemispheres": hemisphere(browser),
        "last_modified": dt.datetime.now()
    }

    browser.quit()
    driver.quit()

    return data

if __name__ == "__main__":
    
    # if running as a script, print the scraped data
    print(scrape_all())