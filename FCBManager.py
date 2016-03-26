from bs4 import BeautifulSoup
from selenium import webdriver
from collections import defaultdict
import os, schedule, time, datetime

import matplotlib.pyplot as plt
import matplotlib.dates as mpdates
from matplotlib import ticker

from config import *
from emailer import send_email


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
    email_subject = "FCB Daily Log | "+str(datetime.date.today())
    with open('accountlog.txt', 'r') as accountlog:
        account_body = accountlog.read()
    data_today = account_body
    send_email("vgooljar@gmail.com", email_subject, data_today) # put last and add image of graph

    data_body = account_body + 'Date: '+str(datetime.date.today())
    data_body = data_body.replace('\n', '|')
    data_body = data_body.replace(': ', ':')
    data_body = data_body.replace('$', '')
    data_body = data_body.replace(',', '')

    with open('datalog.txt', 'a+') as datalog:
        datalog.write(data_body+'\n')

    account_data = []
    with open('datalog.txt', 'r') as datalog:
        account_data = datalog.read().splitlines()

    num_days = sum(1 for line in account_data)

    account_dict = defaultdict(list)

    for day in account_data:
        day_data = day.split("|")
        for account_info in day_data:
            account_parse = account_info.split(':')
            account_dict[account_parse[0]].append(account_parse[1])

    dict_key = list(account_dict.keys()) #[0] is dates, rest is accounts

    dates = account_dict[dict_key[0]]
    x = [datetime.datetime.strptime(d,'%Y-%m-%d').date() for d in dates]

    for i in range(1, len(dict_key)):
        plt.clf()
        account_money = account_dict[dict_key[i]]

        plt.plot(x,account_money)
        # beautify the x-labels
        plt.title(dict_key[i])
        plt.ylabel('Amount Available ($)')
        plt.xlabel('Date (dd/mm/yyyy)')

        plt.gca().yaxis.set_major_formatter(ticker.FormatStrFormatter('%.2f'))

        plt.gca().xaxis.set_major_formatter(mpdates.DateFormatter('%d/%m/%Y'))
        plt.gca().xaxis.set_major_locator(mpdates.DayLocator())
        plt.gcf().autofmt_xdate()

        figname = "graphs/fig"+str(i)+".png"

        plt.savefig(figname, bbox_inches='tight')
        #plt.show()

    if num_days < 30:
        pass
    else:
        pass


'''
schedule.every().hour.do(checkbank)
schedule.every().day.at("8:30").do(dailylog)

while True:
    schedule.run_pending()
    time.sleep(1)
'''
#checkbank()
dailylog()