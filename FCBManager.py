from bs4 import BeautifulSoup
from config import *
from selenium import webdriver
#from selenium.webdriver.support.select import Select
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
#------------------------------------------------------------------------
'''
maidenname = browser.find_element_by_name('mothersMaidenName')
maidenname.send_keys(account_maidenname)

email = browser.find_element_by_name('email')
email.send_keys(account_email)

phonenumber = browser.find_element_by_name('mobilePhoneNumber')
phonenumber.send_keys(account_phonenumber)

pin = browser.find_element_by_name('transactionPin')
pin.send_keys(account_pin)

tpin = browser.find_element_by_name('transactionPinVerify')
tpin.send_keys(account_pin)


hint = browser.find_element_by_name('hint')
hint.send_keys(account_hint)

secretQuest = Select(browser.find_element_by_id("secretQuestion"))
secretQuest.select_by_value(account_secretquestion)

secretAns = browser.find_element_by_name('secretAnswer')
secretAns.send_keys(account_secretanswer)

form = browser.find_element_by_id('noautocomplete')
form.submit()

print browser.page_source
'''
 #------------------------------------------------------------------------

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
