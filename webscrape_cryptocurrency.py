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

numberOfIterations = 0
def write_prices(data_list):
    """sets the entries of the GUI to the currency's real price
    """
    global numberOfIterations
    global iterationLabel
    numberOfIterations+=1
    iterations.set('iterations: '+str(numberOfIterations))
    time.set('last updated: '+str(datetime.datetime.now().time())[:-7])
    for i in range(len(data_list)):
        entryTextPointers[i].set(data_list[i])
        #display price change
        if len(prevPriceList)!=0:
            diff = float(data_list[i])-float(prevPriceList[i])
            changeLabelsList[i].set(round(diff, 3))
    

def start_scraping():
    """scrapes the web urls for the price of each cryptocurrency
    """
    uClientList = []
    htmlList = []
    global priceList, prevPriceList
    
    #access the website and construct a list of uClients' data
    for url in urlList:
        uClient = uReq(url)
        uClientList.append(uClient)
        htmlList.append(uClient.read())
        uClient.close

    pageSoupList = []
    for html in htmlList:
        pageSoupList.append(soup(html, "html.parser"))

    priceList = []
    #extract the price out of the pageSoup
    for pageSoup in pageSoupList:
        priceList.append(str(pageSoup.findAll("span",{"id":"quote_price"})).split()[6][23:-7])

    write_prices(priceList) #call function to display new text
    prevPriceList = priceList[:]
    
scrape_again = 1 #initialize to some value
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
    scrape_again = frame.after(20000, start_infinite) #every 20 seconds

def stop_infinite(event):
    """ends the scraping scheduling loop
    """
    frame.after_cancel(scrape_again)

#GUI
root = Tk()
frame = Frame(root)
root.title("Crytocurrency Updater")

iterations = StringVar()
time = StringVar()
currencyEntryList = []
entryTextPointers = []
columnCount=0
for currency in currencyList:
    entryText = StringVar()
    entryTextPointers.append(entryText)

    Label(frame, text='{}'.format(currency)).grid(row=0,column=columnCount)
    currencyEntry = Entry(frame, textvariable=entryText)
    currencyEntry.grid(row=1, column=columnCount, padx = 5, pady=0)
    currencyEntryList.append(currencyEntry)

    columnCount+=1

#start scraping button
startButton = Button(frame, text='start scraping')
startButton.bind('<Button-1>', base)
startButton.grid(row = 3, column=0, sticky=W, padx=10, pady=4)

#stop scraping button
endButton = Button(frame, text='stop scraping')
endButton.bind('<Button-1>', stop_infinite)
endButton.grid(row = 4, column=0, sticky=W, padx=10)

#show change since last 20 seconds
Label(frame, text='20(s) change:').grid(row=2, column=0, sticky=W, padx=5)
changeLabelsList = []
columnCount2=0
for currency in currencyList:
    priceChange = StringVar()
    changeLabelsList.append(priceChange)
    Label(frame, textvariable=priceChange).grid(row=2, column=columnCount2, sticky=E, padx=3)
    priceChange.set('0.0')
    columnCount2 += 1

#show number of iterations
iterationLabel = Label(frame, textvariable=iterations)
iterationLabel.grid(row=5, column=0, sticky=W, padx=5)
iterations.set('iterations: 0')

#show last updated
updatedLabel = Label(frame, textvariable=time)
updatedLabel.grid(row=5, column=1, sticky=W)
time.set('last updated:')

frame.pack()

root.mainloop()
