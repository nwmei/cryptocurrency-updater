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

#iterations = StringVar()
number = 0
def write_prices(data_list):
    """sets the entries of the GUI to the currency's real price
    """
    global number
    global iterationLabel
    number+=1
    iterations.set('iterations: '+str(number))
    for i in range(len(data_list)):
        entryTextPointers[i].set(data_list[i])

def start_scraping():
    """scrapes the web urls for the price of each cryptocurrency
    """
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
    write_prices(data_list) #call function to set entries to real price
    
    #determine whether or not a price has changed
    global priceList, prevPriceList
##        if priceList != prevPriceList:
##            print('~One of the prices just changed!')
    prevPriceList = priceList[:]
    

scrape_again = 1
#infinite
def base(event):
    """function that calls a scheduling function to scrape again
    """
    start_infinite()
    
def start_infinite():
    """scheduling function to scrape again
    """
    m = start_scraping()
    global scrape_again
    scrape_again = frame.after(7000, start_infinite)

def stop_infinite(event):
    """ends the scraping loop
    """
    print(scrape_again)
    frame.after_cancel(scrape_again)

#GUI
root = Tk()
frame = Frame(root)
root.title("Crytocurrency Updater")

iterations = StringVar()
currencyEntryList = []
entryTextPointers = []
columnCount=0
for currency in currencyList:
    entryText = StringVar()
    entryTextPointers.append(entryText)

    Label(frame, text='{}'.format(currency)).grid(row=0,column=columnCount)
    currencyEntry = Entry(frame, textvariable=entryText)
    currencyEntry.grid(row=1, column=columnCount, padx = 5, pady=5)
    currencyEntryList.append(currencyEntry)

    columnCount+=1

#start scraping button
startButton = Button(frame, text='start scraping')
startButton.bind('<Button-1>', base)
startButton.grid(row = 2, column=0, sticky=W, padx=10, pady=4)

#stop scraping button
endButton = Button(frame, text='stop scraping')
endButton.bind('<Button-1>', stop_infinite)
endButton.grid(row = 3, column=0, sticky=W, padx=10)

#show number of iterations
iterationLabel = Label(frame, textvariable=iterations)
iterationLabel.grid(row=4, column=0, sticky=W)
iterations.set('iterations: 0')

frame.pack()

root.mainloop()
