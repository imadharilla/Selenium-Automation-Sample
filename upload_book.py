from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os 
import pickle
import json

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains

class BookUploader:
	"""docstring for BookUploader"""
	def __init__(self ):
		super(BookUploader, self).__init__()
		self.current_path = os.path.dirname(os.path.realpath(__file__)) + '/'
	
	def generate_browser(self):
		self.driver = webdriver.Edge(executable_path='C:\Projects\Scrapy\KDP\Driver\msedgedriver.exe')
		self.cookies_path = os.path.dirname(os.path.realpath(__file__)) + '/cookies.pkl'

	def close_browser(self):
		self.driver.close()

	def save_cookie(self):
	    with open(self.cookies_path, 'wb') as filehandler:
	        pickle.dump(self.driver.get_cookies(), filehandler)

	def load_cookie(self):
	     with open(self.cookies_path, 'rb') as cookiesfile:
	         cookies = pickle.load(cookiesfile)
	         for cookie in cookies:
	             self.driver.add_cookie(cookie)

	def load_json_data(self):
		with open('amour.json') as json_file:
			books = json.load(json_file)
			json_file.close()
		return books

	def login(self):
		try:
			email = self.driver.find_element_by_id('ap_email')
			email.send_keys('your_email@gmail.com') 
		except:
			pass
		password = self.driver.find_element_by_id('ap_password')
		password.send_keys('your_password')
		sleep(0.3)
		self.driver.find_element_by_id('signInSubmit').click()
	
	def fill_from_1(self, book):
		# Select Language
		language_selector = WebDriverWait(self.driver, 30).until(EC.presence_of_element_located((By.XPATH, '//*[@id="language-field"]/div[1]/span/span/button')))
		language_selector.click()
		language_list = self.driver.find_element_by_xpath('//*[@id="ui-id-1"]')
	
		french_selector = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="ui-id-1"]/li[3]')))
		action1 = ActionChains(self.driver)
		action1.move_to_element(french_selector)
		action1.click()
		action1.perform()

		
		Ftitle = self.driver.find_element_by_xpath('//*[@id="data-title"]')
		Ftitle.clear()
		sleep(0.2)
		Ftitle.send_keys(book['title'])

		Fauthor_name = self.driver.find_element_by_xpath('//*[@id="data-primary-author-first-name"]')
		Fauthor_name.clear()
		Fauthor_name.send_keys('Emelie')

		Fauthor_last_name = self.driver.find_element_by_xpath('//*[@id="data-primary-author-last-name"]')
		Fauthor_last_name.clear()
		Fauthor_last_name.send_keys(book['id'])

		Fdescription = self.driver.find_element_by_xpath('//*[@id="data-description"]')
		Fdescription.clear()
		Fdescription.send_keys(book['description'])

		# publish right
		self.driver.find_element_by_xpath('//*[@id="non-public-domain"]').click()

		# keywords
		for i in range(7):
			try:
				Fkey = self.driver.find_element_by_xpath('//*[@id="data-keywords-'+ str(i) + '"]')
				Fkey.clear()
				Fkey.send_keys(book['tags'][i])
			except:
				break

		# categories
		self.driver.find_element_by_xpath('//*[@id="data-categories-button-proto-announce"]').click()
		sleep(1)

		xpath_1 = '//ul[@id="category-chooser-root-list"]'
		xpath_1 += f'//a[contains(text(), "Fiction")]' # dynamic
		a = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, xpath_1)))
		actions = ActionChains(self.driver)
		actions.move_to_element(a)
		actions.click()
		actions.perform()

		Romance = '//*[@id="div-fiction_romance"]/span/a'
		a = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, Romance)))
		action2 = ActionChains(self.driver)
		action2.move_to_element(a)
		action2.click()
		action2.perform()
		sleep(1)
		self.driver.find_element_by_xpath('//*[@id="checkbox-fiction_general"]').click()
		self.driver.find_element_by_xpath('//*[@id="checkbox-fiction_romance_general"]').click()
		sleep(0.5)
		# submit categories
		self.driver.find_element_by_xpath('//*[@id="category-chooser-ok-button"]/span/input').click()

		# save and continue
		sleep(3)
		self.driver.find_element_by_xpath('//*[@id="save-and-continue-announce"]').click()


	def fill_from_2(self, book):
		# upload doc file
		upload_doc_path = '//*[@id="data-assets-interior-file-upload-AjaxInput"]'
		doc_input = WebDriverWait(self.driver, 60).until(EC.presence_of_element_located((By.XPATH, upload_doc_path)))
		doc_input.send_keys(self.current_path + str(book['id'])+'.docx')

		# upload image file
		image_upload_option = self.driver.find_element_by_xpath('//*[@id="data-cover-choice-accordion"]/div[2]/div/div[1]/a')
		action = ActionChains(self.driver)
		action.move_to_element(image_upload_option)
		action.click()
		action.perform()
		upload_image_path = '//*[@id="data-assets-cover-file-upload-AjaxInput"]'
		image_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.XPATH, upload_image_path)))
		image_input.send_keys(self.current_path + str(book['id'])+'.jpg')

		# save and continue
		sleep(20)
		try:
			self.driver.find_element_by_xpath('//*[@id="save-and-continue-announce"]').click()
		except:
			sleep(10)
			self.driver.find_element_by_xpath('//*[@id="save-and-continue-announce"]').click()
		
	def fill_form_3(self):
		kdpSelect_path = '//*[@id="data-is-select"]'
		kdpSelect = WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.XPATH, kdpSelect_path)))
		kdpSelect.click()
		self.driver.find_element_by_xpath('//*[@id="data-digital-royalty-rate"]/div/div/div[2]/div/label/input').click()
		price = self.driver.find_element_by_xpath('//*[@id="data-digital-us-price-input"]/input')
		price.send_keys('2.99')
		
		# save and publish book
		sleep(3)
		self.driver.find_element_by_xpath('//*[@id="save-and-publish-announce"]').click()

	def upload_book(self, book):
		path = '//input[@aria-labelledby="create-digital-button-announce"]'
		new_book = WebDriverWait(self.driver, 200).until(EC.presence_of_element_located((By.XPATH, path)))
		new_book.click()


		self.fill_from_1(book)

		self.fill_from_2(book)

		self.fill_form_3()

	def upload_all_books(self):
		books = self.load_json_data()
		self.generate_browser()
		# try:
		# 	self.load_cookie()
		# except:
		# 	print("Couldn't load cookies!")

		self.driver.get('https://kdp.amazon.com/en_US/bookshelf')
		try:
			self.login()
			sleep(10)
			self.save_cookie()
		except:
			pass
		self.save_cookie()
		for book in books:
			self.upload_book(book)




uploader = BookUploader()
uploader.upload_all_books()


