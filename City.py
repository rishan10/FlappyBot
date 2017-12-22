import selenium
from selenium import webdriver
from selenium.webdriver.support import ui
from selenium.webdriver.common.keys import Keys
import time

class Game:

	DRIVER = 'chromedriver'
	driver = None

	previousX = None
	previousY = None
	previousTimeCalledX = None
	previousTimeCalledY = None

	previousScore = None

	actions = [0, 1]

	def init(self):
		self.driver = webdriver.Chrome(self.DRIVER)
		self.driver.get('http://flappybird.io/')
		self.previousX = self.driver.execute_script('return bird.x')
		self.previousY = self.driver.execute_script('return bird.y')
		self.previousTimeCalledX = time.time()
		self.previousTimeCalledY = time.time()

		self.previousScore = self.driver.execute_script('return counter.text')

		

	def quit(self):
		try:
			self.driver.quit(self)
		except Exception as e:
			print("quit with exception: ")

	def getXBirdLocation(self):
		x = self.driver.execute_script('return bird.x')
		self.previousX = x
		self.previousTimeCalledX = time.time()
		return x
	def getYBirdLocation(self):
		y = self.driver.execute_script('return bird.y')
		self.previousY = y
		self.previousTimeCalledY = time.time()
		return y



	def getHorizontalVelocity(self):
		deltax = self.driver.execute_script('return bird.x') - self.previousX
		deltat = time.time() - self.previousTimeCalledX
		return deltax/deltat
	def getVerticalVelocity(self):
		deltay = self.driver.execute_script('return bird.y') - self.previousY
		deltat = time.time() - self.previousTimeCalledY
		return deltay/deltat
	def playerIsDead(self):
		return self.driver.execute_script('return dead')
	def hitRestart(self):
		self.driver.execute_script('restart()')

	def getPipeXMidPoint(self):
		return self.driver.execute_script('return pipe.x')

	def getPipeYMidPoint(self):
		gap = self.driver.execute_script('return gap')
		gap = gap/2
		return self.driver.execute_script('return pipe.y') - gap

	def flap(self):
		self.driver.find_element_by_id('testCanvas').click()

	def closeableAdIsPlaying(self):
		try:
			self.driver.find_element_by_id('cpmstart_closeLink_')
			return True
		except Exception as e:
			return False
		return True

	def getRidOfClosaebleAd(self):
		self.driver.find_element_by_id('cpmstart_closeLink_').click()
		

	def videoAdIsPlaying(self):
		try:
			self.driver.find_element_by_class_name('vast-blocker')
			return True
		except Exception as e:
			return False
		return True

	def scoreIncreased(self):
		currentScore = self.driver.execute_script('return counter.text')
		if(currentScore > self.previousScore):
			previousScore = currentScore
			return True
		return False










