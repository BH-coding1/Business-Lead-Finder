import selenium
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException,ElementNotInteractableException,StaleElementReferenceException
from selenium_stealth import stealth
import os
from dotenv import load_dotenv
import random,time
import json
import csv
from selenium.webdriver.support import expected_conditions as EC
import re
import unicodedata
import pandas as pd
class Google_maps_lead_scraper:
    def __init__(self):
        self.all_divisions_list = []
        self.all_business_names_list = []
        self.all_reviews_list= []
        self.business_socials_list = []
        self.business_type_list =[]
        self.business_phone_number_list = []
        self.business_website_list =[]
        self.business_street_list =[]
        self.business_city_list = []
        self.all_number_of_reviews_list = []
        self.url = 'https://www.google.com/maps/'
        options = Options()
        options.add_experimental_option('detach',True)
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/115.0')
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--disable-infobars')
        options.add_argument('--disable-extensions')
        options.add_argument("--start-maximized")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        self.driver = webdriver.Chrome(options=options)
        self.driver.get(url=self.url)


    def wait(self,a,b):
        time.sleep(random.uniform(a=a,b=b))
    def input_business_and_location(self,text):
        self.wait(1.5,2)
        try :
            self.input = self.driver.find_element(By.CLASS_NAME,'searchboxinput')
            self.wait(1.5,2)
            self.input.send_keys(text,Keys.ENTER)
        except (ElementNotInteractableException ,NoSuchElementException,StaleElementReferenceException):
            print('Error in finding element')
            pass


    def get_all_divs(self):
        self.wait(1.5, 2)
        try:
            self.wait(1.5, 2)
            self.all_divisions =self.driver.find_elements(By.CLASS_NAME,'hfpxzc')
        except (ElementNotInteractableException ,NoSuchElementException,StaleElementReferenceException):
            print('Error in finding element')
            pass


    def scroll(self,amount_of_scrolls):
        self.wait(4, 5)
        try:
            self.wait(2, 2.5)
            panel = self.driver.find_element(By.XPATH,'//div[@role="feed"]')
            for scroll in range(amount_of_scrolls):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight',panel)
                self.wait(2,2.5)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException,Exception)as e:
            print('Error in finding element',e)
            pass


    def scrape_business_name(self):
        try:
            self.wait(1.5, 2)
            business_name = self.driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[1]/h1')
            self.all_business_names_list.append(business_name.text)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException) as e :
            self.all_business_names_list.append('N/A' )
            print('Error in finding element',e)
            pass


    def scrape_business_review(self):
        try:
            self.wait(2,2.5)
            review = self.driver.find_element(By.XPATH,'/html/body/div[1]/div[3]/div[8]/div[9]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[1]')
            self.all_reviews_list.append(review.text.split('(')[0]) if review.text else 'N/A'
            self.all_number_of_reviews_list.append(review.text.split('(')[1].split(')')[0])
            print(self.all_reviews_list)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException,Exception)as e:
            self.all_number_of_reviews_list.append('N/A')
            print('Error in finding element',e)
            pass


    def scroll_business_details(self,amount_of_scrolls):
        self.wait(2, 2.5)
        try:
            self.wait(1.5, 2)
            panel = self.driver.find_element(By.XPATH, '//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]')
            for scroll in range(amount_of_scrolls):
                self.driver.execute_script('arguments[0].scrollTop = arguments[0].scrollHeight', panel)
                self.wait(2, 2.5)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            print('Error in finding element', e)
            pass


    def press_on_each_business_link_and_scrape_details(self):
        try :
            self.all_divisions = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
            for i in range(len(self.all_divisions)):
                self.wait(2, 2.2)
                all_divisions = self.driver.find_elements(By.CLASS_NAME, 'hfpxzc')
                self.driver.execute_script("arguments[0].scrollIntoView(true);", all_divisions[i])
                self.driver.execute_script("arguments[0].click();", all_divisions[i])


                self.wait(2, 2.5)

                self.scrape_business_name()
                self.scrape_business_review()
                self.scroll_business_details(1)
                self.scrape_business_type()
                self.scrape_business_website()
                self.scrape_business_location()
                self.scrape_business_phone_number()

            print(self.all_reviews_list)
            print(self.business_type_list)
            print(self.business_street_list)
            print(self.business_city_list)
            print(self.business_website_list)
            print(self.business_phone_number_list)

        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            print('Error in finding element', e)
            pass



    def scrape_business_type(self):
        try:
            self.wait(1.5, 2)
            business_type = self.driver.find_element(By.XPATH,'//*[@id="QA0Szd"]/div/div/div[1]/div[3]/div/div[1]/div/div/div[2]/div[2]/div/div[1]/div[2]/div/div[2]/span[1]/span/button')
            self.business_type_list.append(business_type.text)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            self.business_type_list.append('N/A')
            print('Error in finding element', e)
            pass

    def clean_text(self,text):
        if text is None:
            return 'N/A'
        text = str(text).strip()
        if text.lower() in ['none', 'nan', '', 'n/a']:
            return 'N/A'
        text = unicodedata.normalize('NFKD', text)
        text = ''.join(
            c for c in text
            if unicodedata.category(c)[0] != 'C' and not unicodedata.name(c, '').startswith('PRIVATE USE')
        )
        text = re.sub(r'[^\x20-\x7E]', '', text)
        text = text.replace('\n', ' ').replace(')', '').strip()
        return text
    def clean_phone(self,text):
        if not text or str(text).strip().lower() in ['none', 'nan', '', 'n/a']:
            return 'N/A'
        text = self.clean_text(text)
        text = text.replace('+1 ', '').replace('+1', '')
        return text.strip() if text else 'N/A'
    def scrape_business_location(self):
        try:
            self.wait(1.5, 2)
            business_location = self.driver.find_element(By.XPATH,'//button[contains(@data-item-id,"address")]')
            self.business_street_list.append(business_location.text.split(',')[0])
            self.business_city_list.append(business_location.text.split(',')[1])
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            self.business_street_list.append('N/A')
            self.business_city_list.append('N/A')
            print('Error in finding element', e)
            pass


    def scrape_business_website(self):
        try:
            self.wait(1.5, 2)
            business_website = self.driver.find_element(By.XPATH,'//a[contains(@aria-label, "Website")]').get_attribute('href')
            self.business_website_list.append(business_website)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            self.business_website_list.append('N/A')
            print('Error in finding element', e)
            pass


    def scrape_business_phone_number(self):
        try:
            self.wait(1.5, 2)
            phone_number = self.driver.find_element(By.XPATH, '//button[contains(@data-item-id,"phone")]')
            clean = self.clean_phone(phone_number.text)
            self.business_phone_number_list.append(clean)
        except (ElementNotInteractableException, NoSuchElementException, StaleElementReferenceException, Exception) as e:
            self.business_phone_number_list.append('N/A')
            print('Error in finding element', e)
            pass

    def export_to_csv(self):
        with open('Lead_Data.csv','w',newline='', encoding='utf-8') as file:
            csv_writer = csv.writer(file, quoting=csv.QUOTE_MINIMAL)
            csv_writer.writerow([
                'Business Name',
                'Business Type',
                'Phone Number',
                'Website',
                'Review Score',
                'Number of Reviews',
                'Street',
                'Location'
            ])
            for line in range(len(self.all_divisions)):
                name = self.clean_text(self.all_business_names_list[line] )if line < len(self.all_business_names_list) else ""
                business_type = self.clean_text(self.business_type_list[line] )if line < len(self.business_type_list) else ""

                phone_number = self.business_phone_number_list[line].replace("+1 ", "").replace("+1", "") if line < len(
                    self.business_phone_number_list) else ""

                website = self.clean_text(self.business_website_list[line]) if line < len(self.business_website_list) else ""
                review = self.clean_text(self.all_reviews_list[line]) if line < len(self.all_reviews_list) else ""
                review_count = self.clean_text(self.all_number_of_reviews_list[line]) if line < len(
                    self.all_number_of_reviews_list) else ""
                street = self.clean_text(self.business_street_list[line]) if line < len(self.business_street_list) else ""
                city = self.clean_text(self.business_city_list[line]) if line < len(self.business_street_list) else ""
                csv_writer.writerow([
                    name, business_type, phone_number, website, review, review_count, street,city
                ])
    def clean_lists(self):
        min_len = min(
            len(self.all_business_names_list),
            len(self.business_type_list),
            len(self.business_phone_number_list),
            len(self.business_website_list),
            len(self.all_reviews_list),
            len(self.all_number_of_reviews_list),
            len(self.business_street_list),
            len(self.business_city_list)
        )


        self.all_business_names_list = [self.clean_text(i) for i in self.all_business_names_list[:min_len]]
        self.business_type_list = [self.clean_text(i) for i in self.business_type_list[:min_len]]
        self.business_phone_number_list = [i.replace("+1 ", "").replace("+1", "") for i in
                                           self.business_phone_number_list[:min_len]]
        self.business_website_list = [self.clean_text(i) for i in self.business_website_list[:min_len]]
        self.all_reviews_list = [self.clean_text(i) for i in self.all_reviews_list[:min_len]]
        self.all_number_of_reviews_list = [self.clean_text(i) for i in self.all_number_of_reviews_list[:min_len]]
        self.business_street_list = [self.clean_text(i) for i in self.business_street_list[:min_len]]
        self.business_city_list = [self.clean_text(i) for i in self.business_city_list[:min_len]]
    def export_to_spreadsheet(self):
        try:
            df = pd.DataFrame({
            "Business Name": self.all_business_names_list,
            "Business Type": self.business_type_list,
            "Phone Number": self.business_phone_number_list,
            "Website": self.business_website_list,
            "Review Score": self.all_reviews_list,
            "Number of Reviews": self.all_number_of_reviews_list,
            "Street": self.business_street_list,
            "Location": self.business_city_list
            })
            df.to_excel('Lead_Data.xlsx',index=False,engine='openpyxl')
        except ValueError :
            pass