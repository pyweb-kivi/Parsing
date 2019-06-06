from selenium import webdriver
from time import sleep

class Bot:

	def __init__(self):
		self.driver = webdriver.Firefox()
		self.navigate()

	def navigate(self):
		n = 2
		pages = []
		#self.driver.get("https://it.kompass.com/searchCompanies?acClassif=&localizationCode=&localizationLabel=&localizationType=&text=%22Impianti+di+osmosi+inversa+per+il+trattamento+delle+acque%22&searchType=SUPPLIER")
		self.driver.get("https://it.kompass.com/en/searchCompanies?acClassif=&localizationCode=&localizationLabel=&localizationType=&text=%22Lift+trucks%2C+second-hand%22&searchType=SUPPLIER")
		sleep(5)
		total_pages = self.driver.find_elements_by_xpath("//ul[@class='pagination paginatorDivId']/li")[-2].text
		all_links = self.driver.find_elements_by_xpath("//div[@id='resultatDivId']//h2/a")
		for i in all_links:
			pages.append(i.get_attribute("href"))
		while n < (int(total_pages) + 1):
			try:
				if n < (int(total_pages) + 1):
					button = self.driver.find_element_by_xpath("//ul[@class='pagination paginatorDivId']/li[@class='active']/following-sibling::li/a")
					button.click()
					sleep(8)
					all_links = self.driver.find_elements_by_xpath("//div[@id='resultatDivId']//h2/a")
					for i in all_links:
						pages.append(i.get_attribute("href"))
					print("Page - " + str(n) + " --> " + self.driver.current_url + " --len-- " + str(len(pages)))
					n += 1
			except:
				print()
				print(len(pages))
				for i in pages:
					print(i)

		#print(pages)
		print()
		print(len(pages))
		for i in pages:
				print(i)


def main():
	b = Bot()

if __name__ == '__main__':
	main()
