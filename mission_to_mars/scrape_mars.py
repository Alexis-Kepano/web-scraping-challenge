# Dependencies
import pandas as pd
from splinter import Browser
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
import pymongo
import time
# Initialize PyMongo to work with MongoDBs
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
def scrape_info():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Visit the mars nasa news site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # Optional delay for loading the page
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    slide_elem = news_soup.select_one('ul.item_list li.slide')
    slide_elem.find("div", class_='content_title')
    # Use the parent element to find the first `a` tag and save it as `news_title`
    news_title = slide_elem.find("div", class_='content_title').get_text()
    news_title
    # Use the parent element to find the paragraph text
    news_p = slide_elem.find('div', class_="article_teaser_body").get_text()
    news_p
    # Visit URL
    mars_img_url_list=[]
    base_url='https://www.jpl.nasa.gov'
    mars_url = '/images?search=&category=Mars'
    #visits first web page
    browser.visit(base_url+mars_url)
    #gives time for the browser to load
    time.sleep(2)
    #select Topic
    #checks the Mars topic
    browser.find_by_css("input[id=filter_Mars]").first.click()
    time.sleep(3)
    #gets the html code of the page
    html2=browser.html
    time.sleep(2)
    #turns the html into beautiful soup
    mars_topic_soup=bs(html2,'html.parser')
    #returns a list of mars topic images on this visited webpage
    search_listing_page_results=mars_topic_soup.find_all('div',class_="SearchResultCard")[0]
    #concatenates base_url with image url
    first_mars_topic_img_url=base_url+search_listing_page_results.a['href']
    #gets title
    first_mars_topic_img_title=search_listing_page_results.h2.text
    print(first_mars_topic_img_title)
    #visits the nasa page with the high resolution URL
    browser.visit(first_mars_topic_img_url)
    time.sleep(2)
    #get the html code for that high resolution url page
    html3=browser.html
    #turns that html code into some beautiful soup
    high_res_soup=bs(html3,'html.parser')
    #splits and slices string of different img links from the attribute 'srcset' for the highest resolution link
    high_res_img_website=high_res_soup.find_all('img',class_='BaseImage')[0]['srcset'].split()[-2]
    #produces full website
    print(high_res_img_website)
    #print(html3)
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'
    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)
    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]
    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']
    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)
    # Save html code to folder Assets
    mars_table = mars_df.to_html()
    mars_table = mars_table.replace('\n', '')
    # Display mars_df
    mars_df
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)
    #gives time for the browser to load
    time.sleep(2)
    # HTML Object
    html_hemispheres = browser.html
    # Parse HTML with Beautiful Soup
    soup = bs(html_hemispheres, 'html.parser')
    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')
    # Create empty list for hemisphere urls 
    hemisphere_image_urls = []
    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov'
    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = bs( partial_img_html, 'html.parser')
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        # Append the retreived information into a list of dictionaries 
        hemisphere_image_urls.append({"title" : title, "img_url" : img_url})
    # Display hemisphere_image_urls
    hemisphere_image_urls
    browser.quit()
    mars_dict = {
        'news_title': news_title,
        'news_paragraph': news_p,
        'featured_image': high_res_img_website,
        'mars_table': mars_table,
        'mars_hemispheres': hemisphere_image_urls
    }   
    print(mars_dict)
    return mars_dict 