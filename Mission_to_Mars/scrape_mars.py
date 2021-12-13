from bs4 import BeautifulSoup as bs
import requests
import pandas as pd

# tool for browsing with Spliter
from webdriver_manager.chrome import ChromeDriverManager
from splinter import Browser


def scrape():
#	initiate the dictionary; use this dictionary to insert into the database later	
	scrape_dict = {}


#		1)--------SCRAPE FOR LATEST NEWS' TITLE AND PARAGRAPH
	# set up request
	news_url = 'https://mars.nasa.gov/news/'
	response = requests.get(news_url)
	# create soup object
	soup = bs(response.text, 'html.parser')

	# scrape for title:
	title_result = soup.find('div', class_='content_title')
	news_title = title_result.text
	#scape for paragraph:
	teaser_result = soup.find('div', class_='rollover_description_inner')
	teaser_para = teaser_result.text


#		2)------- SCRAPE FOR FEATURED IMAGE:
	# Set up Splinter
	executable_path = {'executable_path': ChromeDriverManager().install()}
	browser = Browser('chrome', **executable_path, headless = False)

	# browse the link 
	img_url = 'https://spaceimages-mars.com/'
	browser.visit(img_url)
	html = browser.html
	soup = bs(html, 'html.parser')
	# click on the buttone "Full image"
	browser.links.find_by_partial_text('FULL IMAGE').click()
	
	# overwrite the html variable to run on the new page after the click
	html = browser.html
	soup = bs(html, 'html.parser')
	soup.find('img', class_='fancybox-image')['src']
	# Store the image url into a variable
	feature_image_url = f"{img_url}{soup.find('img', class_='fancybox-image')['src']}"

#		3)----------  MARS FACTS:
	fact_url = 'https://galaxyfacts-mars.com/'
	tables = pd.read_html(fact_url)
	# Mars's facts
	mars_facts_df = tables[1]
	mars_facts_df.columns = ["Entities", "Info"]
	# Mars and Earth comparision facts
	mars_earth_df = tables[0]

#		4)------------ SCRAPE FOR MARS' HEMISPHERES:
	hami_url = 'https://marshemispheres.com/'
	browser.visit(hami_url)
	# save the list of links that have the word "Enhanced" into the list
	links_found = browser.links.find_by_partial_text('Enhanced')

	# inititate a list to save all the iamge URLs later
	image_urls = []
	
	for i in range(4): 
	#     click on the link with associate order of i
		links_found[i].click()

	#     find the word 'Enhanced' and click on the link
		browser.links.find_by_text('Sample').click()

	#     the click on the link pop-up another window
	#     Therefore, need to bring the current session to second window
		browser.windows.current = browser.windows[1]

	#     reset html variable and soup variable, cuz at the end the whole found_links list is changed
		html = browser.html
		soup = bs(html, 'html.parser')

	#     save the url into image variable
		image = soup.find('img')['src']
	#     save the link into list/dictioary as needed
		image_urls.append(image)


	#     back to the first window
		window = browser.windows[0]
	#     close all other window
		window.close_others()
	#     bring the browser session back to first window
		browser.windows.current = browser.windows[0]

	#     get back to the main page with hami_url on the first window
		browser.visit(hami_url)
	#     find all the links with 'Enhanced' again
		links_found = browser.links.find_by_partial_text('Enhanced')
	
	# quit Chrome, save energy, ram and maintaining good practice
	browser.quit()

	hemisphere_image_urls = [{"title": "Valles Marineris Hemisphere"},
    							{"title": "Cerberus Hemisphere"},
    							{"title": "Schiaparelli Hemisphere"},
    							{"title": "Syrtis Major Hemisphere"}]
	pointer = 0
	for title_dict in hemisphere_image_urls:
	    title_dict.update({'img_url': image_urls[pointer]})
	    pointer += 1

#	store all the scraped info into 1 dictionary: (I hope that I'm right)
	mars_scrape_dictionary = {'Latest News': news_title, 
    'News Paragraph': teaser_para, 
    'Featured Image': feature_image_url,
    'Facts': mars_earth_df,
    'Hemisphere URLs': hemisphere_image_urls}

#-------------- RETURN SOMETHING
	return mars_scrape_dictionary











