from selenium import webdriver # webdriver for chrome
from shutil import which # to find the path of the chromedriver
import time # for sleep function
from selenium.webdriver.chrome.options import Options # for headless browser
from scrapy.selector import Selector # for converting string to selector
import pandas as pd # for creating dataframe


#setting up  driver
#chrome_options = Options()
#chrome_options.add_argument("--headless")

chrome_path = which("chromedriver-win64\chromedriver.exe") #to find the path of the chromedriver

driver = webdriver.Chrome(executable_path= chrome_path ) #,options= chrome_options)

# link to page for reviews
driver.get("https://www.amazon.in/Samsung-Midnight-Storage-6000mAh-Battery/dp/B0B4F52B5X/ref=sr_1_19?crid=3MYYKX0NNPSZH&keywords=phone&qid=1691068012&sprefix=phone%2Caps%2C1450&sr=8-19")


driver.set_window_size(1920, 1080) # setting window size

time.sleep(3)

see_all_reviews = driver.find_element_by_xpath("//a[@data-hook = 'see-all-reviews-link-foot']")



# clicking on page to load reviews
see_all_reviews.click()

time.sleep(5)

# scraping data of critical reviews first

orignial_url = driver.current_url


# selecting  reviews dropdown
recent_reviews_dropdown = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[2]/span/span/span/span")
# clicking dropdown
recent_reviews_dropdown.click()

# selecting critical reviews
recent_reviews= driver.find_element_by_xpath("/html/body/div[3]/div/div/ul/li[9]")

# clicking critical reviews
recent_reviews.click()
time.sleep(5)

# verifying crtified purchase
certified_purchase = driver.find_element_by_xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[3]/div[2]/div[2]/div[1]/span/span/span/span")
certified_purchase.click() 

time.sleep(5)
# clicking verified purchase 
verified_purchase = driver.find_element_by_xpath("/html/body/div[3]/div/div/ul/li[2]/a")
verified_purchase.click()
time.sleep(5)



# getting html markup of page
first_page =  driver.page_source

# converting to selector
first_page_selector = Selector(text= first_page)

# creating dictionary to store data
my_critical_dict ={"date":[] , "star": [], "heading" : [] , "review" :[]}

# function to get data from pages 
def scrap_pages_cri(page):
    global my_critical_dict
    blocks =  page.xpath("/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[@class = 'a-section review aok-relative']")

    for parts in blocks:
        date =  parts.xpath(".//span[@data-hook = 'review-date']//text()").get()
        head=  parts.xpath(".//a[@data-hook = 'review-title']//span[2]//text()").get()
        rating =  parts.xpath(".//a[@data-hook = 'review-title']//i[@data-hook = 'review-star-rating']//span[@class = 'a-icon-alt']//text()").get()
        review =  parts.xpath(".//span[@data-hook = 'review-body']//span//text()").getall()

        my_critical_dict["date"].append(date)
        my_critical_dict["star"].append(rating)
        my_critical_dict["heading"].append(head)
        my_critical_dict["review"].append(review)


        time.sleep(2)

x = 0 # number of pages to scrap 
scrap_pages_cri(first_page_selector)
while(x< 10 ):

    

    # getting next page button
      # getting next page button
    try:

        next= driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[12]/span/div/ul/li[2]/a')
        next.click()
    except:
        next =  driver.find_element_by_xpath('/html/body/div[1]/div[3]/div/div[1]/div/div[1]/div[5]/div[3]/div/div[12]/span/div/ul/li[2]')
        next.click()


    time.sleep(5)

    second_page =  driver.page_source 
    second_page_selector = Selector(text= second_page)

    scrap_pages_cri(second_page_selector)
    x = x+1

final_data= pd.DataFrame.from_dict(my_critical_dict)
final_data.to_csv("critical_amazon.csv")

driver.quit()