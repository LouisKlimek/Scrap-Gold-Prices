import math
import re
import urllib
from urllib.request import urlopen, Request
import os
from pathlib import Path
from datetime import datetime
import random
import time
import browser
from bs4 import BeautifulSoup
import goldDE

#Change this to .com or whatever if you are not from Germany
ebayDomain = "ebay.de"

searchTerm = "goldkette"

# Gold Types have to be in lowercase!!
goldTypes = ["24k", "22k", "21,6k", "21k", "18k", "14k", "9k","8k","999", "916", "900", "875", "750", "585", "375","333"]

goldTypeConverter = {
    "999": "24k",
    "916": "22k",
    "900": "21,6k",
    "875": "21k",
    "750": "18k",
    "585": "14k",
    "375": "9k",
    "333": "8k"
}

# GET GOLD PRICES AT STARTUP
print("--GETTING GOLD PRICES--")
goldTypePricesGrammEuro = {
    "24k": "0",
    "22k": "0",
    "21,6k": "0",
    "21k": "0",
    "18k": "0",
    "14k": "0",
    "9k": "0",
    "8k": "0"
}

for goldType in goldTypePricesGrammEuro.keys():
    try:
        goldTypePricesGrammEuro[goldType] = str(goldDE.getGoldPrice(goldType,"EUR","gramm"))
        print(goldType + ": " + goldTypePricesGrammEuro[goldType]+"€/g")
    except:
        print(goldType + ": Could not get Price.")
print("--GETTING GOLD PRICES DONE--")

# Blacklisted Words have to be in lowercase!!
blacklistedWords = ["beschichtet", "vergoldet", "modeschmuck", "plated", "bi-Color", "imitat", "silber", "goldfarbe",
                    "ungeprüft", "ungetestet", "unecht", "fake", "dekoration", "ausstellstück", "ausstellung", "deko","untestet","unchecked","gold-plated","gilded"]

for i in range(1, 10):
    # GET HTML
    html = ""
    for line in urlopen(
            Request("https://www." + ebayDomain + "/sch/i.html?LH_ItemCondition=3000|10&_nkw=" + searchTerm + "&_pgn=" + str(i),
                    headers={
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})):
        html += line.decode("utf-8")
    parsed_html = BeautifulSoup(html, features="html.parser")

    # LOOP THROUGH ALL LISTED ITEMS
    for item in parsed_html.body.findAll('li', attrs={'class': 's-item'}):
        oK = True
        try:
            itemUrl = \
            item.findChildren("div")[0].findChildren("div", attrs={'class': 's-item__info'})[0].findChildren("a")[0][
                'href']
        except:
            print("!!!ERROR WHILE GETTING ITEM URL!!!")
            oK = False

        if oK:
            # Get Item HTML
            try:
                itemHtml = browser.getHtml(itemUrl, '//*[@id="desc_div"]')
                parsed_item_html = BeautifulSoup(itemHtml, features="html.parser")
            except:
                print("!!!ERROR WHILE GETTING ITEM HTML!!")
                oK = False

            if oK:
                print("URL: " + itemUrl)

                # Get Item Price
                try:
                    # If there is an error in getting the Price by the id "prcIsum" its an Auction and not a Buy Now
                    itemPrice = parsed_item_html.body.findAll('span', attrs={'id': 'prcIsum'})[0].text
                    itemAuctionType = "Buy Now"
                except:
                    itemPrice = parsed_item_html.body.findAll('span', attrs={'id': 'prcIsum_bidPrice'})[0].text
                    itemAuctionType = "Bidding"

                # Check if accepts offers
                try:
                    # If the Send Offer button is found the item accepts offers
                    parsed_item_html.body.findAll('a', attrs={'id': 'boBtn_btn'})[0]
                    itemAcceptsOffers = True
                except:
                    itemAcceptsOffers = False

                # Get Shipping Costs
                try:
                    itemShippingCost = parsed_item_html.body.findAll('span', attrs={'id': 'fshippingCost'})[0].findChildren("span")[0].text
                except:
                    itemShippingCost = ""

                # Get Remaining Time
                try:
                    itemRemainingTime = parsed_item_html.body.findAll('span', attrs={'id': 'vi-cdown_timeLeft'})[0].text
                except:
                    itemRemainingTime = ""

                # Get Title
                itemTitle = parsed_item_html.body.findAll('h1', attrs={'id': 'itemTitle'})[0].text.replace("Details zu   ", "")

                # Get Description
                itemDescriptionURL = parsed_item_html.findAll('div', attrs={'id': 'desc_div'})[0].findChildren("iframe")[0]['src']

                itemDescription = ""
                try:
                    itemDescription = " ".join(BeautifulSoup(browser.getHtml(itemDescriptionURL, '/html'),
                                                             features="html.parser").body.get_text().split())
                except:
                    print("!!!ERROR WHILE GETTING ITEM DESCRIPTION!!")

                itemExtraInfo = ""
                try:
                    # itemExtraInfo is only in rare cases present -> Put in a tryCatch
                    itemExtraInfo = parsed_item_html.body.findAll('span', attrs={'class': 'topItmCndDscMsg'})[0].text
                except:
                    pass

                # Change Gramm,etc. to g
                itemInfoComplete = (itemTitle + " " + itemExtraInfo + " " + itemDescription).lower().replace(' gramm','g').replace(' gr', 'g').replace(' g', 'g').replace('gramm', 'g').replace('gr', 'g')
                # Change ounce,etc. to ℥
                itemInfoComplete = itemInfoComplete.replace(' oz', '℥').replace(' ounce', '℥').replace(' unze','℥').replace('oz', '℥').replace('ounce', '℥').replace('unze', '℥')
                # Change karat,etc. to k
                itemInfoComplete = itemInfoComplete.replace(' karat', 'k').replace(' ct', 'k').replace(' k','k').replace('karat', 'k').replace('ct', 'k')
                # Remove Double Spaces
                itemInfoComplete = itemInfoComplete.replace('  ', ' ').replace('  ', ' ')
                # Remove JavaScript end thingy
                itemInfoComplete = itemInfoComplete.split("var _rfr", 1)[0]
                # Change , to .
                itemInfoComplete = itemInfoComplete.replace(",", ".")
                # Remove other junk stuff
                itemInfoComplete = itemInfoComplete.replace("§ 312g", "").replace("gebraucht", "").replace("gelbgold", "").replace("gold", "")

                blacklistedWordFound = False
                for word in blacklistedWords:
                    if itemInfoComplete.find(word) >= 0:
                        print("!!!BLACKLISTED WORD FOUND | GOING TO NEXT ITEM!!!")
                        blacklistedWordFound = True
                        break
                if blacklistedWordFound:
                    continue

                # Get weight of item
                foundItemWeights = []
                number = ""
                for char in list(itemInfoComplete):
                    if char.isdigit() or ((char == "," or char == "." or char == "/") and number != ""):
                        number += char
                    else:
                        # eval() in case weight is given in e.g. 100/500 Ounce, 100/500 Gramm
                        if number != "" and char == "g":
                            foundItemWeights.append(float(str(eval(number))))
                        if number != "" and char == "℥":
                            # CALCULATE fine ℥ TO GRAMM
                            foundItemWeights.append(float(str(eval(number))) * 31.1034768)
                        number = ""

                # Get smallest weight found in Item Description/Title
                foundItemWeights.sort()
                itemWeight = str(*foundItemWeights[:1]) + "g"

                # GET GOLD TYPE
                itemGoldType = ""
                for goldType in goldTypes:
                    if itemInfoComplete.find(goldType) >= 0:
                        itemGoldType = goldType
                        break
                # CONVERT GOLD TYPE TO KARATS
                if itemGoldType != "" and itemGoldType[-1] != "k":
                    itemGoldType = goldTypeConverter[itemGoldType]

                # GET ITEM WORTH
                itemWorth = ""
                if itemWeight[:-1] != "" and itemGoldType != "":
                    itemWorth = float(goldTypePricesGrammEuro[itemGoldType]) * float(itemWeight[:-1])

                print("Weight: " + str(itemWeight))
                print("Purity: " + itemGoldType)
                print("Worth: " + str(itemWorth))
                print("Current Price: " + str(itemPrice))
                print("Shipping Cost: " + str(itemShippingCost))
                print("Auction Type: " + itemAuctionType)
                print("Accepts Offers: " + str(itemAcceptsOffers))
                print("Remaining Time:" + itemRemainingTime)
                print("Item Info: " + itemInfoComplete)
                print("---------------------------------------------")