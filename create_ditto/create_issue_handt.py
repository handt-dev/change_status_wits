#!/usr/bin/python3
from selenium import webdriver
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
from selenium.webdriver.common.keys import Keys
def access_nss_list(nss_link):
	mydriver.get(nss_link)

def get_issue_list():
	total = mydriver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[1]/div[1]/span/span[3]").text
	total = int(total) + 1
	a  = list(range(1, total))
	print("PPR have total {} issue".format(total))
	for i in a:
		print("Checking issue ",i)
		bms_link = 'https://wits.dzsi.net/browse/'
		root_xpath = "/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[2]/div/issuetable-web-component/table/tbody/tr[{}]"
		ditto_id = mydriver.find_element_by_xpath(root_xpath.format(i)+"/td[4]").text
		issue_id = mydriver.find_element_by_xpath(root_xpath.format(i))
		rel_id = issue_id.get_attribute("rel")
		ditto_id = ditto_id.find("NOSVG")
		if ditto_id > -1:
			print("Already created ditto, next")
		else : 
			print("Please create ditto")
			bms_id = mydriver.find_element_by_xpath(root_xpath.format(i)+"/td[1]").text
			print(bms_id)
			url_bms = bms_link + bms_id
			bms_title = mydriver.find_element_by_xpath(root_xpath.format(i)+"/td[2]").text
			print(bms_title)

			priority_type = mydriver.find_element_by_xpath(root_xpath.format(i)+"/td[5]/img")
			priority = priority_type.get_attribute("alt") # datatype string
			print(priority)

			issue_type = mydriver.find_element_by_xpath(root_xpath.format(i)+"/td[7]/a/img")
			issue_type = issue_type.get_attribute("alt") # datatype string
			print(issue_type)

			url_create = "https://wits.dzsi.net/secure/CreateIssue!default.jspa"
			mydriver.get(url_create)

			add_issue_type = mydriver.find_element_by_id('issuetype-field')
			add_issue_type.clear()
			time.sleep(2)
			add_issue_type.send_keys(issue_type)
			time.sleep(2)
			add_issue_type.send_keys(Keys.TAB)
			time.sleep(2)

			mydriver.find_element_by_xpath("//input[@name='Next']").click()

			title_wits = mydriver.find_element_by_id('summary') 
			title_wits.send_keys(bms_title)

			add_priority = mydriver.find_element_by_id('priority-field')
			add_priority.clear()
			time.sleep(2)
			add_priority.send_keys(priority)
			time.sleep(2)
			add_priority.send_keys(Keys.TAB)
			time.sleep(2)

			Fix_Version = mydriver.find_element_by_id('fixVersions-textarea')
			Fix_Version.send_keys('{}'.format(fixversion))

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

if __name__ == '__main__':
	print("Input NSS link: (View in Issue Navigator)")
	nss_link = input()
	print("\nInput milestone (ex: [GPON2][Oversea_FIBRAIN]H660GM-A_EN7528_ER-IT): ")
	milestone = input()
	print("\nInput fix version (ex: [GPON2][Oversea_FIBRAIN]H660GM-A_EN7528_ER-IT): ")
	fixversion = input()
	browser = webdriver.FirefoxProfile('/home/handt/.mozilla/firefox/6vjcmo6u.default-release')
	mydriver = webdriver.Firefox(browser)
	mydriver.get("https://wits.dzsi.net/browse/NOSVG-20165")
	access_nss_list(nss_link)
	get_issue_list()
	mydriver.close()
#	mydriver.exit()