from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import sys

chrome_options = Options()  
chrome_options.add_argument("--headless")  
browser = webdriver.Chrome("../../../chromedriver", chrome_options = chrome_options)

#enter horse names into the below list in quotes, separated by commas. eg. ["red rum","arkle"]
horses = []

class Horse_tipper():
	def get_dosage(self,horses):
		browser.get("https://www.pedigreequery.com/")
		for horse in horses:
			browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[1]/input").send_keys(horse)

			try:
				browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[5]/input").click()
				details = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/center/table[1]/tbody/tr/td[1]/center/font").text
				
				print(horse, details[details.rfind("DI"):])
			
			except:
				options = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/blockquote/table/tbody").text
				print(options)
				horse_num = input("What is the index of the horse")

				if int(horse_num) > 1:
	
					browser.get("https://www.pedigreequery.com/{}{}".format(horse, horse_num))
					details = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/center/table[1]/tbody/tr/td[1]/center/font").text
				
				else:
					browser.get("https://www.pedigreequery.com/{}".format(horse))
					details = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/center/table[1]/tbody/tr/td[1]/center/font").text

				
				print(horse, details[details.rfind("DI"):])
	
tip = Horse_tipper()
print(tip.get_dosage(horses))
