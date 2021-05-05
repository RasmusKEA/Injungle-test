#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests
import pyrebase

firebaseConfig = {
    'apiKey': "AIzaSyAie4Ea5dJcMgEao5jLkyDr17fh8bfI87k",
    'authDomain': "injungltest.firebaseapp.com",
    'databaseURL': "https://injungltest-default-rtdb.firebaseio.com/",
    'projectId': "injungltest",
    'storageBucket': "injungltest.appspot.com",
    'messagingSenderId': "890282536235",
    'appId': "1:890282536235:web:dbd2bb4c6cfb4c401ce96e",
    'measurementId': "G-GW4XFFVNBG"
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
# auth=firebase.auth()
# storage=firebase.storage()

productList = []


def getProducts(link, productList):
    base = 'https://www.cultbeauty.co.uk'  # siden for hudpleje produkter
    # html for input link struktureres i soup objekt vha html parser
    soup = BeautifulSoup(requests.get(link).text, 'html.parser')
    # find div der indeholder alle sidens produkter
    parent = soup.find_all(
        'div', {'class': 'productGridItem js-product-grid-item'})

    for x in parent:
        # generer links til alle sidens produkter i en liste
        productList += list(map(lambda n: base +
                            n['href'].split('#')[0], x.find_all('a', href=True)))

    print(len(productList))
    return productList


def getData(link):

    def getIngredients(items, text):  # henter alle "kasserne" fra produkt siden
        for item in items:
            # Hvis en "kasse" indeholder Full ingredients list så..
            if item.find('div', {'class': 'itemHeader'}).text.strip() == text.strip():
                # returner ingredienslisten
                return item.find('div', {'class': 'itemContent'})

    def getDetails(node, tag, name):
        return node.find(tag, {'class': name}).text.strip()

    soup = BeautifulSoup(requests.get(link).text, 'html.parser')

    brand = getDetails(soup, 'div', 'productBrandTitle')
    name = getDetails(soup, 'div', 'productTitle')
    size = getDetails(soup, 'span', 'productSize')
    sign = getDetails(soup, 'span', 'productCurrency')
    price = getDetails(soup, 'span', 'productPrice')

    data = {'brand': brand, 'name': name}
    db.child("products").push(data)

    # find alle li tags der indeholder ul tags med klassen productInfoInner
    boxes = soup.find('ul', {'class': 'productInfoInner'}).find_all('li')
    # find den "kasse" der indeholder ingredienserne
    ingredients = getIngredients(boxes, 'Full ingredients list').text

    print(brand, name, sign, price, ingredients, sep=';')

    print('\n')


load_number = 0
while (load_number < 30):
    # /products?loadedAmount=1980  # https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=1980&path=%2Fskin-care.html&parameters=%7B%7D
    products = getProducts('https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=' +
                           str(load_number) + '&path=%2Fskin-care.html&parameters=%7B%7D', productList)
    load_number += 30

for p in products:
    print(getData(p))


# -----------
# def getBrands():
#    base        = 'https://www.cultbeauty.co.uk'
#    soup        = BeautifulSoup(requests.get(base + '/brands').text, 'html.parser') # soup-objekt der indeholder parset html fra brands siden
#    parent      = soup.find('ul', { 'class' : 'brandsList' }) # finder alle ul tags af klassen brandList
#    brands      = list(map(lambda n : base + n['href'].split('?')[0], parent.find_all('a', href = True))) # laver en liste med url adresser (links) for alle brands
#    return brands
