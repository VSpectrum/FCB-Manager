from bs4 import BeautifulSoup
from config import *
from selenium import webdriver
import os

phantomjs = os.path.realpath(os.path.join(os.getcwd(), "phantomjs"))
browser = webdriver.PhantomJS(phantomjs)
url = r"https://www.firstcitizenstt.net/"
browser.get(url)

username = browser.find_element_by_name('userName')
username.send_keys(account_number)
password = browser.find_element_by_name('password')
password.send_keys(account_password)

form = browser.find_element_by_id('noautocomplete')
form.submit()

url = r"https://www.firstcitizenstt.net/accountList.do"
browser.get(url)
response = browser.page_source
soup = BeautifulSoup(response, "html.parser")

#TOTAL BALANCE
total_balance = []
total_balance_type = []
total_balance_amount = []
for td in soup.find_all('div', {'class': 'column'}):
    for span in td.find_all('dt'):
        total_balance_type.append(span.text)
    for span in td.find_all('dd'):
        total_balance_amount.append(span.text)
total_balance = zip(total_balance_type, total_balance_amount)
print total_balance

#GET CURRENT BALANCE
total_available = []
total_available_type = []
total_available_amount = []
alltr =  soup.find_all("tr", {"class":["odd", "even"]},recursive=True)
for tr in alltr:
    #print tr.contents[1].get_text() + " " + tr.contents[-1].get_text()
    total_available_type.append(tr.contents[1].get_text())
    total_available_amount.append(tr.contents[-1].get_text())
total_available = zip(total_available_type, total_available_amount)
print total_available

