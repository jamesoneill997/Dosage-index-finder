from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium import webdriver  
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver.common.keys import Keys
import time
import sys
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import (Mail, Attachment, FileContent, FileName, FileType, Disposition)
import base64

chrome_options = Options()  
chrome_options.add_argument("--headless")  
browser = webdriver.Chrome("../../../chromedriver", options = chrome_options)

#enter horse names into the below list in quotes, separated by commas. eg. ["red rum","arkle"]
horses = ["new safuhdisaoh new me"]
f = open("output.txt", 'w+')

class Horse_tipper():
	def get_dosage(self,horses):
		results = []
		browser.get("https://www.pedigreequery.com/")
		for horse in horses:
			browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[1]/input").send_keys(horse)

			try:
				browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[6]/input").click()
				time.sleep(1.2)
				details = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/center/table[1]/tbody").text				
				results.append(horse + " " + details[details.rfind("DI"):])
			
			except:
				options = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/blockquote/table/tbody").text
				print(options)
				horse_num = input("What is the index of the horse? ")

				if int(horse_num) > 1:
	
					browser.get("https://www.pedigreequery.com/{}{}".format(horse, horse_num))
					details = browser.find_element_by_xpath("/html/body/table/tbody/tr[5]/td[1]/center/table[1]/tbody/tr/td[1]/center/font").text
				
				else:
					browser.get("https://www.pedigreequery.com/{}".format(horse))
					details = "DI: UNKNOWN CD: UNKNOWN"

				
				results.append(horse + " " + details[details.rfind("DI"):])
		
		

		#write result
		for result in results:
			f.write(result + "\n")

	def get_horses(self, url):
		horses = []
		jockeys = []

		browser.get(url)
		time.sleep(1)
		runners = browser.find_elements_by_class_name("name")

		for result in runners:
			horse, jockey = str(result.text).split("\n")

			horses.append(horse)
			jockeys.append(jockey)
		
		return horses
	
	def send_mail(self, race):
		#create txt file
		self.get_dosage(self.get_horses(race))
		time.sleep(10)

		with open('output.txt', 'rb') as f:
			data = f.read()
			encoded_file = base64.b64encode(data).decode()

			

			attached_file = Attachment(
				FileContent(str(encoded_file)),
				FileName('output.txt'),
				FileType('txt'),
				Disposition('attachment')
			)

			message = Mail(
				from_email='jamesoneill997@gmail.com',
				to_emails='jamesoneill997@gmail.com',
				subject='race',
				html_content='<p>See attached</p>')
		
			message.attachment = attached_file

			f.close()
		try:
			sg = SendGridAPIClient(os.environ.get('SENDGRID'))
			response = sg.send(message)
			print(response.status_code)
			print(response.body)
			print(response.headers)
		except Exception as e:
			print(e)



tip = Horse_tipper()

tip.send_mail(input("Please paste the market URL here: "))