import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import pymongo
import datetime as dt

def scrape_all():
    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    data = {
        "news_title": news_title,
        "news_paragraph": news_paragraph,
        "featured_image": mars_featured(browser),
        "hemispheres": hemispheres(browser),
        "weather": mars_twitter_weather(browser),
        "facts": mars_facts(),
        "last_modified": dt.datetime.now()
    }
    browser.quit()

    return data

def mars_news(browser):

    #Website Article Title
    url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    browser.visit(url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    news_title = soup.find("div", class_='list_text').find("div", class_="content_title").text
    print(news_title)
    news_paragraph = soup.find("div", class_="article_teaser_body").text
    
    return news_title, news_paragraph

def mars_featured(browser):

    #Featured Image
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image = soup.find("div", class_="carousel_container").find("div", class_="carousel_items")
    img = featured_image.find("article", class_="carousel_item")["style"]
    img

    featured_image_url = jpl_url + '/spaceimages/images/wallpaper/PIA23170-1920x1200.jpg'
    
    return featured_image_url
    
def mars_twitter_weather(browser):

    #Weather from Twitter
    twitter_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(twitter_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    mars_weather = soup.select_one(".js-tweet-text-container").find("p").text
    
    return mars_weather
  

def mars_facts():
    
    #Space Facts Website
    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)
    tables

    df = tables[0]

    df.columns = ['Parameters', 'Values']
    df

    html_table = df.to_html()
    html_table

    facts_html_table = html_table.replace('\n', '')
    
    return facts_html_table

def hemispheres(browser):

    #Hemisphere Images
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    image_urls = []
    source_url = 'https://astrogeology.usgs.gov'
    items = soup.find_all("div", class_="item")

    for item in items:
        title = item.find("h3").text
        partial_img_url = item.find('a', class_='itemLink product-item')['href']
        browser.visit(source_url + partial_img_url)
        partial_img_url = browser.html
        soup = BeautifulSoup(partial_img_url, "html.parser")
        full_img = source_url + soup.find('div', class_='downloads').find('a')['href']
        
        image_urls.append({"title": title, "image_url": full_img})

    return image_urls

if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


