from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def scrape():
    results_dict = {}
    executable_path = {'executable_path': r'C:\workspace\Resources\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    # NASA Mars News ------------------------------------------------------------
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    # titles=[]
    # bodies=[]
    # html = browser.html
    # soup = bs(html, 'html.parser')
    time.sleep(1)
    html = browser.html 
    soup = bs(html, 'html.parser')
    news_title = soup.find("div", class_="content_title").text
    news_p = soup.find("div", class_="article_teaser_body").text

    #results = soup.find_all(class_='slide')
    #for result in results[:20]:
    # news_title = soup.find('div', class_='content_title').text
    # news_p = soup.find('div',class_='article_teaser_body').text
        #titles.append(title)
        #bodies.append(body)
        #print(title)
        #print(body)
    #try:
        #browser.click_link_by_partial_text('more')    
   # except:
       # print("Scraping Complete")

    #news_title= titles[0]
    #news_p= bodies[0]

    results_dict['news_title'] = news_title
    results_dict['news_p'] = news_p

    ### JPL Mars Space Images - Featured Image

    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    image_list=[]
    for x in range(1, 2):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_image = soup.find_all('article',class_='carousel_item')
        for image in mars_image:
            print('page:', x, '-------------')
            print(image)
            image_list.append(image)
        try:
            browser.click_link_by_partial_text('more')    
        except:
            print("Scraping Complete")
    images= image_list[0]['style'].split("'")[1]
    beginn='https://www.jpl.nasa.gov'
    featured_image_url = beginn+images

    results_dict['featured_image_url'] = featured_image_url

    # Mars Weather------------------------------------------------------------
    ### Mars Weather

    url_weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(url_weather)
    weathers=[]
    for x in range(1, 2):
        html = browser.html
        soup = bs(html, 'html.parser')
        mars_weather = soup.find_all(class_='js-tweet-text-container')
        for weather in mars_weather:
            print('page:', x, '-------------')
            print(weather)
            weathers.append(weather)
        try:
            browser.click_link_by_partial_text('more')    
        except:
            print("Scraping Complete")

    unwanted_link=weathers[0].find('p').find('a').get_text()
    mars_weather= weathers[0].find('p').text.replace(unwanted_link,'').replace('\n','')

    results_dict['mars_weather'] = mars_weather

    # Mars Facts------------------------------------------------------------
    url_facts='https://space-facts.com/mars/'
    time.sleep(1)
    tables = pd.read_html(url_facts)
    df=tables[1]
    df.columns=['Mars Profile','Figures']
    df.set_index('Mars Profile', inplace=True)
    mars_df= df.reset_index().to_html(index = False)

    results_dict['mars_df'] = mars_df

    ### Mars Hemispheres

    hemis_url= 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemis_url)
    soup = bs(browser.html, 'html.parser')

    hemisphere_image_urls = []

    results_hemis = soup.find_all('div', class_='item')

    for item in results_hemis:
        title_hemis = item.h3.text
        first_url = hemis_url[:30] + item.find('a', class_='itemLink')['href']
        browser.visit(first_url)
        soup = bs(browser.html, 'html.parser')
        time.sleep(1)
        final_url = hemis_url[:30] + soup.find('img', class_='wide-image')['src']
        hemisphere_image_urls.append({'title': title_hemis, 'img_url':final_url})

    results_dict['hemisphere_image_urls'] = hemisphere_image_urls

    return results_dict