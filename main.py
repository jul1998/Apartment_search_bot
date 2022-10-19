import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import bs4
import requests

chrome_driver_path = Service("../ChromeDriver/chromedriver.exe")
op = webdriver.ChromeOptions()

URL = "https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos/heredia-provincia?q=f_rent.150000-450000"
#URL = "https://www.encuentra24.com/costa-rica-es/bienes-raices-alquiler-apartamentos?regionslug=san-jose-provincia-san-jose-capital-san-sebastian,san-jose-provincia-san-jose-capital-san-francisco-de-dos-rios,san-jose-provincia-san-jose-capital-pavas&q=f_rent.150000-325000"
FORM_URL = "https://docs.google.com/forms/d/e/1FAIpQLScNUyd1Yy9AvQT-LBlV_SDTWmnDvs43vHVUtehVCfsYU9stVw/viewform?usp=sf_link"
page = requests.get(URL)
#
# soup = bs4.BeautifulSoup(page.content, "html.parser")

class Apartments:
    def __init__(self):
        self.page = requests.get(URL)
        self.soup = bs4.BeautifulSoup(page.content, "html.parser")
        self.apartment_titles_list = []
        self.apartment_description_list = []
        self.apartment_prices_list = []
        self.apartment_locations = []
        self.apartment_links = []
        self.driver = webdriver.Chrome(service=chrome_driver_path, options=op)


    def get_titles(self):
        raw_apartment_titles = self.soup.find_all(class_="ann-ad-tile__title")
        self.apartment_titles_list = [apartment_title.text.strip() for apartment_title in raw_apartment_titles]
        print(self.apartment_titles_list)


    def get_descriptions(self):
        raw_apartment_descriptions = self.soup.find_all(class_="ann-ad-tile__short-description")
        self.apartment_description_list = [apartment_description.text.strip() for apartment_description in
                                      raw_apartment_descriptions]
        print(self.apartment_description_list)


    def get_prices(self):
        raw_apartment_price = self.soup.find_all(class_="ann-ad-tile__price")
        self.apartment_prices_list = [apartment_price.text.strip().replace(",","") for apartment_price in raw_apartment_price]
        print(self.apartment_prices_list)

    def get_addresses(self):
        raw_aparment_addresses = self.soup.find_all(class_="ann-ad-tile__footer-item")
        apartment_address_list = [address.text.strip() for address in raw_aparment_addresses]
        self.apartment_locations = [location for index, location in enumerate(apartment_address_list) if index % 2 != 0]
        print(self.apartment_locations)

    def get_links(self):
        raw_apartment_links = self.soup.find_all(class_="ann-ad-tile__title")
        self.apartment_links = []
        for title in raw_apartment_links:
            link = title.get("href")
            functional_link = f"https://www.encuentra24.com/{link}"
            self.apartment_links.append(functional_link)
        print(self.apartment_links)



    def autofill_form(self):
        self.driver.get(FORM_URL)
        time.sleep(2)
        for index  in range(len(self.apartment_titles_list)):
            time.sleep(2)
            title_entry = self.driver.find_element(By.XPATH, "//div[@class='lrKTG']//div[1]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
            title_entry.click()
            title_entry.send_keys(self.apartment_titles_list[index])

            description_entry = self.driver.find_element(By.XPATH, "//div[@role='list']//div[2]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
            description_entry.click()
            description_entry.send_keys(self.apartment_description_list[index])


            location_entry = self.driver.find_element(By.XPATH,"//div[@class='teQAzf']//div[3]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
            location_entry.click()
            location_entry.send_keys(self.apartment_locations[index])


            price_entry = self.driver.find_element(By.XPATH,"//div[4]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
            price_entry.click()
            price_entry.send_keys(self.apartment_prices_list[index])


            link_entry = self.driver.find_element(By.XPATH,"//div[5]//div[1]//div[1]//div[2]//div[1]//div[1]//div[1]//div[1]//input[1]")
            link_entry.click()
            link_entry.send_keys(self.apartment_links[index])
            time.sleep(3)


            submit_button = self.driver.find_element(By.XPATH,"//div[@class='uArJ5e UQuaGc Y5sE8d VkkpIf QvWxOd']//span[@class='l4V7wb Fxmcue']")
            submit_button.click()
            time.sleep(3)

            another_response = self.driver.find_element(By.LINK_TEXT,"Enviar otra respuesta")
            another_response.click()




data = Apartments()
data.get_titles()
data.get_descriptions()
data.get_prices()
data.get_addresses()
data.get_links()
data.autofill_form()









