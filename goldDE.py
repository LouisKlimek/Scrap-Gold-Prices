import json
import urllib
from urllib.request import urlopen, Request
import lxml
from lxml import etree, html

fractionConversion = {
    "24k": "999",
    "23k": "958",
    "22k": "916",
    "21,6k": "900",
    "21k": "875",
    "20k": "833",
    "19k": "791",
    "18k": "750",
    "17k": "708",
    "16k": "666",
    "15k": "625",
    "14k": "585",
    "9k": "375",
    "8k": "333"
}

def __getResponse(url):
    data = ""
    for line in urlopen(Request(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'})):
        data += line.decode("utf-8")
    return data


def __getJsonResponse(url):
    jsonData = json.loads(__getResponse(url))
    return jsonData


def getGoldPrice(karat, currency="EUR", unitOfMeasurement="gramm"):
    price = 0
    try:
        karat = fractionConversion[karat] if karat[-1].lower() == "k" else karat
    except KeyError:
        raise Exception("ERROR WHILE CONVERTING KARAT TO WEIGHT PERCENTAGE: THIS KARAT VALUE IS NOT SUPPORTED")

    try:
        parsedData = html.fromstring(__getResponse("https://www.gold.de/verkaufen/altgold/"+karat))
        price = float(parsedData.xpath("//div[@class='bg_weiss r5 fw700 fz26 mfz18 pd5 cdblau']")[0].text[:5].replace(",","."))
    except lxml.etree.ParserError:
        raise Exception("ERROR WHILE GETTING GOLD PRICE: THIS KARAT VALUE IS NOT SUPPORTED OR THE WEBSITE IS DOWN")

    return price
