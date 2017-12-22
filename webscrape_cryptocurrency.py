from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup
import datetime

currencyList = ['bitcoin', 'ripple', 'litecoin', 'ethereum', 'bitcoin-cash']

urlList = []

#create list of Urls depending on currencies above
for currency in currencyList:
    urlList.append('https://coinmarketcap.com/currencies/{}/'.format(currency))

#2 lists of prices to determine whether or not price changed
prevPriceList = []
priceList = []

#continuously output prices
while True:
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
    
    for i in range(len(currencyList)):
        currency = currencyList[i]
        analysis += currency + ': $' + priceList[i] + '   '
    
    print(analysis)

    #determine whether or not a price has changed
    if priceList != prevPriceList:
        print('~One of the prices just changed!')
    prevPriceList = priceList[:]
