from bs4 import BeautifulSoup
from selenium import webdriver
import os, schedule, time

from config import *
from emailer import *

def checkbank():
    phantomjs_executable = ''
    if os.name=='nt': phantomjs_executable = "phantomjs.exe"
    else: phantomjs_executable = "phantomjs"
    phantomjs = os.path.realpath(os.path.join(os.getcwd(), phantomjs_executable))
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

    browser.quit();

    #GET CURRENT BALANCE
    total_available = []
    total_available_type = []
    total_available_amount = []
    alltr =  soup.find_all("tr", {"class":["odd", "even"]},recursive=True)
    for tr in alltr:
        total_available_type.append(tr.contents[1].get_text())
        total_available_amount.append(tr.contents[-1].get_text())
    total_available = zip(total_available_type, total_available_amount)

    email_subject = ""
    email_body = ""
    '''
    for amount in total_balance:
        email_body+= (amount[0]+": "+amount[1]+"\n")
    email_body+="\n"
    '''
    for amount in total_available:
        email_body+= (amount[0]+": "+amount[1]+"\n")
        email_subject += (amount[0]+": "+amount[1]+" | ")

    email_subject = email_subject[:-2] + " - FCB"
    email_subject = "FCB Account Update"

    account_body = ""
    with open('accountlog.txt', 'r') as accountlog:
        account_body = accountlog.read()

    if account_body != email_body:
        with open('accountlog.txt', 'w') as accountlog:
            accountlog.write(email_body)
        send_email("vgooljar@gmail.com", email_subject, email_body)

def dailylog():
    account_body = ''
    with open('accountlog.txt', 'r') as accountlog:
        account_body = accountlog.read()
    send_email("vgooljar@gmail.com", "FCB Daily Log", account_body)

schedule.every().hour.do(checkbank)
schedule.every().day.at("8:30").do(dailylog)

while True:
    schedule.run_pending()
    time.sleep(1)