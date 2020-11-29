#!/usr/bin/python3

# This script is used to change status from FREFIXED TO FIXED and add the fixversion for the issue when release 
# it's also is used to change other file like fix version, epic link, title,...
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
from selenium.webdriver.support import expected_conditions as EC

#nss_link = 'https://wits.dasanzhone.com/issues/?jql=status%20%3D%20prefixed%20AND%20project%20%3D%2011522%20AND%20fixVersion%20%3D%2072124%20ORDER%20BY%20priority%20DESC%2C%20key%20ASC'


def access_nss_list(nss_link):
	mydriver.get(nss_link)

def get_issue_list():
	total_issue = mydriver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[1]/div[1]/span/span[3]").text
	total_issue = int(total_issue)
	a  = list(range(1, total_issue+1))
	for i in a :
		issue_id = mydriver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[2]/div/issuetable-web-component/table/tbody/tr[{}]/td[1]".format(i))
		issue_id_list.append(issue_id.text)
		rel_id = mydriver.find_element_by_xpath("/html/body/div[1]/section/div[1]/div[3]/div/div/div/div/div/div/div[2]/div/issuetable-web-component/table/tbody/tr[{}]".format(i)).get_attribute("rel")
		rel_id_list.append(rel_id)
	print("list of issue",issue_id_list)
#	print("List of rel",rel_id_list)

def change_status():			
	for issue_id in issue_id_list:
		mydriver.get('https://wits.dasanzhone.com/browse/{}'.format(issue_id))
		status = mydriver.find_element_by_id('opsbar-opsbar-transitions').text
		if status == "FIXED" :
			mydriver.find_element_by_id('opsbar-opsbar-transitions').click()
			time.sleep(3) # need to find the better way
		else :
			print("Don't need to change status")

def update_fix_version(fix_version):
	for rel_id in rel_id_list:
		mydriver.get('https://wits.dasanzhone.com/secure/EditIssue!default.jspa?id={}'.format(rel_id))
		Fix_Version = mydriver.find_element_by_id('fixVersions-textarea')
		Fix_Version.send_keys('{}'.format(fix_version))
		time.sleep(3)
		mydriver.find_element_by_id('issue-edit-submit').click()

if __name__ == '__main__':
	issue_id_list = []
	rel_id_list = []
	print("Input NSS list link (View in Issue Navigator): ")
	nss_link = input()
	print("Input Fix version (ex. 2.05-0004.01): ")
	fix_version = input()
	browser = webdriver.FirefoxProfile('/home/handt/.mozilla/firefox/i56wli45.handt/')
	mydriver = webdriver.Firefox(browser)
	access_nss_list(nss_link)
	get_issue_list()
	change_status()
	update_fix_version(fix_version)
