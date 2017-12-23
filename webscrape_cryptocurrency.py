from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime
from tkinter import *
from tkinter import ttk

currencyList = ['bitcoin', 'ripple', 'litecoin', 'ethereum', 'bitcoin-cash']
urlList = []
#create list of Urls depending on currencies above
for currency in currencyList:
    urlList.append('https://coinmarketcap.com/currencies/{}/'.format(currency))
    
#2 lists of prices to determine whether or not price changed
prevPriceList = []
priceList = []

def write_prices(data_list):
    for i in range(len(data_list)):
        entryTextPointers[i].set(data_list[i])
        #currencyEntryList[i].insert(0, data_list[i])

def start_scraping():
    #continuously output prices
    #while True:
    uClientList = []
    htmlList = []

    #access the website and construct a list of uClients' data
    for url in urlList:
        uClient = uReq(url)
        uClientList.append(uClient)
        htmlList.append(uClient.read())
        uClient.close

    pageSoupList = []
    for html in htmlList:
        pageSoupList.append(soup(html, "html.parser"))

    for pageSoup in pageSoupList:
        priceList.append(str(pageSoup.findAll("span",{"id":"quote_price"})).split()[6][23:-7])

    #extract the price out of the pageSoup
    analysis = 'Time: ' + str(datetime.datetime.now().time())[:-7] + '.........'

    data_list = []
    for i in range(len(currencyList)):
        currency = currencyList[i]
        analysis += currency + ': $' + priceList[i] + '   '
        data_list.append(priceList[i])
    
    write_prices(data_list)
    #return analysis
    #currencyEntryList[0].insert(0,analysis)
    #determine whether or not a price has changed
    global priceList, prevPriceList
##        if priceList != prevPriceList:
##            print('~One of the prices just changed!')
    prevPriceList = priceList[:]
    

scrape_again = 1
#infinite
def base(event):
    start_infinite()
    
def start_infinite():
    m = start_scraping()
    global scrape_again
    scrape_again = root.after(7000, start_infinite)

def stop_infinite(event):
    print(scrape_again)
    root.after_cancel(scrape_again)

#GUI
root = Tk()
root.title("Crytocurrency Updater")

currencyEntryList = []
entryTextPointers = []
for currency in currencyList:
    entryText = StringVar()
    entryTextPointers.append(entryText)
    
    Label(root, text='{}'.format(currency)).pack(side=LEFT)
    currencyEntry = Entry(root, textvariable=entryText)
    currencyEntry.pack(side=LEFT)
    currencyEntryList.append(currencyEntry)

#start scraping button
startButton = Button(root, text='start scraping')
startButton.bind('<Button-1>', base)
startButton.pack(side=BOTTOM)

#stop scraping button
endButton = Button(root, text='stop scraping')
endButton.bind('<Button-1>', stop_infinite)
endButton.pack(side=LEFT)

root.mainloop()
