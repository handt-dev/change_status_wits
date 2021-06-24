#!/usr/bin/python3
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.firefox.options import Options	
from selenium.common.exceptions import *
import time
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from time import sleep
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.wait import WebDriverWait


class CreateIssueCommon(object):
	"""docstring for """
	def __init__(self,fixversion=None, milestone=None, root_xpath=None):
		self.fixversion = fixversion
		self.milestone = milestone
		self.root_xpath = "/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[2]/div/issuetable-web-component/table/tbody/"
	def access_nss_list(self):
		mydriver.get(nss_link)
		return

	def get_issue_list(self):
		
		total = mydriver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[1]/div[1]/span/span[3]").text
		print("List have total {} issue".format(total))
		number_issue  = list(range(1, (int(total)+1)))
		print("List of items: ")
		for i in number_issue:
			ppr_key = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[1]".format(i)).text
			summary = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[2]".format(i)).text
			print("{} - {} ".format(ppr_key,summary))
		return number_issue,ppr_key,summary

	def create_issue(self,number_issue,ppr_key,summary):
		print("Input milestone (ex: [GPON2][Oversea_FIBRAIN]H660GM-A_EN7528_ER-IT: ")
		milestone = input()
		print("Input fix version (ex: [GPON2][Oversea_FIBRAIN]H660GM-A_EN7528_ER-IT: ")
		fixversion = input()
		for i in number_issue:
			print("Checking issue ",ppr_key)
			#wits_link = 'https://wits.dzsi.net/browse/'
			#ppr_key = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[1]".format(i)).text
			#summary = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[2]".format(i)).text
			nosvg_linked_id = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[4]".format(i)).text
			priority_el = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]/td[5]/img".format(i))
			priority_id = priority_el.get_attribute("alt")
			issue_id = mydriver.find_element_by_xpath(self.root_xpath+"tr[{}]".format(i))
			rel_id = issue_id.get_attribute("rel") # Need this value to edit			
			nosvg_linked_id = nosvg_linked_id.find("NOSVG")
			if nosvg_linked_id > -1:
				print("Already created NOSVG issue for RnD, next")
			else : 
				print("Starting to create NOSVG issue for {}-{} ".format(ppr_key,summary))
				#print(ppr_key)
				url_bms ='https://wits.dzsi.net/browse/'+ppr_key
				#print(summary)
				url_create = "https://wits.dzsi.net/secure/CreateIssue!default.jspa"
				mydriver.get(url_create)
				mydriver.find_element_by_xpath("//input[@name='Next']").click()
				title_wits = mydriver.find_element_by_id('summary') 
				title_wits.send_keys(summary) 
				priority = mydriver.find_element_by_id('priority-field')
				priority.clear()
				priority.click()
				priority.send_keys(priority_id)
				#priority.send_keys(Keys.TAB)
				time.sleep(1)

				Fix_Version = mydriver.find_element_by_id('fixVersions-textarea')
				Fix_Version.send_keys(fixversion)
				time.sleep(1)

				Assignee = mydriver.find_element_by_id('assign-to-me-trigger')
				time.sleep(1)
				Assignee.click()
				time.sleep(1)
				Assignee.click()

				js = "document.getElementById('description').value = '{}';".format(url_bms)
				mydriver.execute_script(js)
				time.sleep(2)
				el = mydriver.find_element_by_id('customfield_10842')
				for option in el.find_elements_by_tag_name('option') :
					if option.text == '[Open] {}'.format(milestone) :
						option.click()
						break
				mydriver.find_element_by_id('issue-create-submit').click()

				# link issue bms to wits
				new_issue = mydriver.current_url
				print(mydriver.current_url)
				NOSVG = mydriver.current_url[-11:]
				print(NOSVG)
				# Edit bms to link wits
				url_edit = 'https://wits.dzsi.net/secure/EditIssue!default.jspa?id={}'.format(rel_id)
				mydriver.get(url_edit)
				linked_issue = mydriver.find_element_by_id('issuelinks-issues-textarea')
				linked_issue.send_keys(NOSVG)
				time.sleep(2)
				mydriver.find_element_by_id('issue-edit-submit').click()
				mydriver.get(url_bms)
				mydriver.get(new_issue)
				mydriver.get(nss_link)


def main():
	print("Starting to running script....")
	print("Input NSS link: (View in Issue Navigator)")
	#mydriver.get("https://wits.dzsi.net/browse/NOSVG-17660")
	nss_link = input()
	mydriver = webdriver.Firefox(webdriver.FirefoxProfile('/home/handt/.mozilla/firefox/i56wli45.handt/'))
	handt = CreateIssueCommon()
	handt.access_nss_list()
	return_value = handt.get_issue_list()
	handt.create_issue(return_value[0],return_value[1],return_value[2])
	mydriver.close()

if __name__ == '__main__':
	main()
