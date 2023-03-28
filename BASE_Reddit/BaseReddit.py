import random
import time

from loguru import logger
from selenium.common import ElementClickInterceptedException
from selenium.webdriver.common.by import By

from Settings_Selenium import BaseClass
from BASE_Reddit.exceptions import NotRefrashPageException, BanAccountException


class BaseReddit(BaseClass):
	def __init__(self):
		super(__class__, self).__init__()

	# -------------------------  ban ------------------------------
	def _baned_account(self):
		logger.info("Check if account banned.")
		self.wait_load_webpage()
		if not self.elem_exists(value='//a[contains(@href, "https://www.reddithelp.com/")]', wait=0.3):
			return

		else:
			raise BanAccountException("Your account banned")

	# ________________________ BASE REDDIT ___________________________
	def _error_cdn_to_server(self):
		if self.elem_exists(value='body', by=By.TAG_NAME, wait=60):
			self.click_element(value='//section/form/button[contains(text(), "Accept all")]', wait=0.3)
			if self.elem_exists('//*[contains(text(), "Our CDN was unable to reach our servers")]', wait=0.1):
				return True
			else:
				return False
		elif self.elem_exists('''//*[contains(text(), "Sorry, for some reason reddit can't be reached.")]'''):
			if self.elem_exists(
					'''//*[contains(text(), "Sorry, for some reason reddit can't be reached.")]''', wait=0.1):
				return True
			else:
				return False
		else:
			logger.warning("Сторінка не завантажилась, беру наступну задачу.")
			return True

	def wait_load_webpage(self):
		logger.info("Wait load page!")
		if not self._error_cdn_to_server():
			logger.info("Loading webpage!")
			return
		else:
			self.refrash_page()
			if not self._error_cdn_to_server():
				return
			else:
				raise NotRefrashPageException("Our CDN was unable to reach our servers")

	####################################### subscribe ###################################
	def _previously_subscribing(self):
		# while not exists button
		if self.elem_exists('//button[contains(@id, "subscribe-button") and contains(text(), "Join")]', wait=1):
			wait = 10
			# while not self.elem_exists('''//button[descendant::span[contains(text(), "Joined")]
			# or descendant::span[contains(text(), "Leave")]]''', wait=wait):
			while not self.click_element(
					'//button[contains(@id, "subscribe-button") and contains(text(), "Join")]',
					wait=wait):

				time.sleep(2)
				wait = 1
				self.DRIVER.refresh()
				self.wait_load_webpage()

				logger.debug("Чекаємо підписки!")
			else:
				logger.debug("Підписка оформлена!!!")
		# elif self.elem_exists('//button[contains(text(), "Follow")]', wait=1):
		#     wait = 0.1
		#     while not self.elem_exists('//button[contains(text(), "Unfollow")]', wait=wait):
		#         self.click_element('//button[contains(text(), "Follow")]', wait=1)
		#         wait = 10
		#         time.sleep(2)
		#     else:
		#         logger.debug("Підписка оформлена")
		else:
			logger.debug("Підписки не було зроблено. Можливо вона вже оформлена.")

	def subscribing(self):
		logger.info("Account is subscribing!")

		try:
			self._previously_subscribing()
		except ElementClickInterceptedException:
			logger.error("ElementClickInterceptedException: subscribing")
			self.subscribing()

		logger.info("Subscribed!")

	# ______________________________ interests _____________________________________
	def _button_continue(self):
		logger.info('Press button "continue"')
		# asks to continue when you visit a site with a post
		if self.click_element('//button[contains(text(), "Continue")]', wait=0.2):
			self.wait_load_webpage()
		else:
			self.click_element('//button[@aria-label="Close"]', wait=1)

	def btn_close_interest(self):
		self.click_element('//button[@aria-label="Close"]', wait=1, intercepted_click=True)

	def _select_communities(self):
		self.elem_exists('//button[contains(text(), "Select All")]')
		count_communities = len(self.DRIVER.find_elements(By.XPATH, '//button[contains(text(), "Select All")]'))

		for _ in range(random.randint(1, count_communities)):
			communities_button = f'//button[contains(text(), "Select All")]'
			self.click_element(value=communities_button, scroll_to=True, wait=1)

		try:
			return self._button_continue()
		except ElementClickInterceptedException:
			self.click_element('//button[@aria-label="Close"]', wait=1, intercepted_click=True)

	def select_interests(self):
		logger.info("Select interests!")
		if self.elem_exists('//div[@role="dialog" and @aria-modal="true"]', wait=0.2):
			num = 0
			if random.randint(0, 4) <= 2:
				for _ in range(random.randint(3, 5)):
					num_selected = random.randint(1, 3)
					num += num_selected
					interest_button = f'//div[@role="dialog"]//button[@role="button"][{num}]'
					self.click_element(value=interest_button, scroll_to=True, wait=1)

				self._button_continue()

				# watch element not fill color
				self.wait_load_webpage()

				return self._select_communities()
			else:
				self.btn_close_interest()
