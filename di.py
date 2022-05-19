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


# TODO - REMOVE DEPENDENCY ON CHROMEDRIVER
# NEED TO EITHER ADD CODE TO DOWNLOAD RELEVANT DRIVER AND PLACE IN CORRECT DIR
# OR
# MOVE AWAY FROM WEB SCRAPING ALTOGETHER AND COME UP WITH A MORE ELEGANT SOLUTION (PREFERRED)

chrome_options = Options()
chrome_options.add_argument("--headless")
browser = webdriver.Chrome("../../../chromedriver", options = chrome_options)

class Horse_tipper():
	def get_dosage(self,horses):
		f = open("output.txt", 'w+')
		results = []
		browser.get("https://www.pedigreequery.com/")
		for horse in horses:
			browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[1]/input").send_keys(horse)

			try:
				browser.find_element_by_xpath("/html/body/table/tbody/tr[2]/td/form/table/tbody/tr/td[6]/input").click()
				time.sleep(1.2) #TODO - REFACTOR TO SLEEP UNTIL ELEM LOADS
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
		f.close()


	def get_horses(self, url):
		horses = []
		jockeys = []

		browser.get(url)
		time.sleep(1) #TODO REFACTOR SLEEP
		runners = browser.find_elements_by_class_name("name")

		for result in runners:
			horse, jockey = str(result.text).split("\n")

			horses.append(horse)
			jockeys.append(jockey)
		
		return horses #TODO ADD PARENTS OF HORSE IN ORDER TO DEPRECATE HAVING TO ENTER INDEX OF HORSE
	
	def send_mail(self):
		#open file
		with open('output.txt', 'rb') as f:
			data = f.read()
			encoded_file = base64.b64encode(data).decode()

			attached_file = Attachment(
				FileContent(encoded_file),
				FileName('output.txt'),
				FileType('txt'),
				Disposition('attachment')
			)

			#create message
			message = Mail(
				from_email='jamesoneill997@gmail.com',
				to_emails='gerfoneill@gmail.com',
				subject='race',
				html_content='<p>See attached</p>')
		
			message.attachment = attached_file

			f.close()
		try:
			sg = SendGridAPIClient(os.environ.get('SENDGRID'))
			response = sg.send(message)
			print(response.status_code)
		except Exception as e:
			print(e)




def main():
	tip = Horse_tipper()
	race = input("Please enter the URL of the market here: ")
	#create txt file
	tip.get_dosage(tip.get_horses(race))

	tip.send_mail()

	if __name__ == '__main__':
main()
