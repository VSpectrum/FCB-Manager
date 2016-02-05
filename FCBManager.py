from bs4 import BeautifulSoup
from Tkinter import *
from config import account_number, account_password
from selenium import webdriver

class TropicalCourier:
    def __init__(self, master):
        master.minsize(width=300, height=300)
        master.maxsize(width=300, height=300)

        frame = Frame(master)
        frame.pack()

        self.gdButton = Button(frame, text="Get Data", command=self.get_data)
        self.gdButton.pack(side=TOP)

        self.showData = Label(frame, text="")
        self.showData.pack(side=BOTTOM)

    def get_data(self):
        browser = webdriver.PhantomJS('phantomjs.exe')
        url = r"https://www.firstcitizenstt.net/login.do?"
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


root = Tk()
TC = TropicalCourier(root)
root.mainloop()
