from bs4 import BeautifulSoup
import requests


def getBrands():
    base        = 'https://www.cultbeauty.co.uk'
    soup        = BeautifulSoup(requests.get(base + '/brands').text, 'html.parser') # soup-objekt der indeholder parset html fra brands siden
    parent      = soup.find('ul', { 'class' : 'brandsList' }) # finder alle ul tags af klassen brandList
    brands      = list(map(lambda n : base + n['href'].split('?')[0], parent.find_all('a', href = True))) # laver en liste med url adresser (links) for alle brands
    return brands

def getProducts(link):
    base        = 'https://www.cultbeauty.co.uk/skin-care.html' # siden for hudpleje produkter
    soup        = BeautifulSoup(requests.get(link).text, 'html.parser') # html for input link struktureres i soup objekt vha html parser
    parent      = soup.find('div', { 'class' : 'productGrid' }) # find div der indeholder alle sidens produkter
    products    = list(map(lambda n : base + n['href'].split('#')[0], parent.find_all('a', href = True))) # generer links til alle sidens produkter i en liste
    return products

def getData(link):
    
    def getIngredients(items, text): #henter alle "kasserne" fra produkt siden
        for item in items:
            if item.find('div', {'class' : 'itemHeader'}).text.strip() == text.strip(): # Hvis en "kasse" indeholder Full ingredients list så..
                return item.find('div', {'class' : 'itemContent'}) # returner ingredienslisten
    
    def getDetails(node, tag, name):
        return node.find(tag, {'class' : name}).text.strip('()')

    soup    = BeautifulSoup(requests.get(link).text, 'html.parser')

    brand   = getDetails(soup, 'div' , 'productBrandTitle'  )
    name    = getDetails(soup, 'div' , 'productTitle'       )
    size    = getDetails(soup, 'span', 'productSize'        )  #AttributeError: 'NoneType' object has no attribute 'text' (se linje 33)
    sign    = getDetails(soup, 'span', 'productCurrency'    )
    price   = getDetails(soup, 'span', 'productPrice'       )
    
    boxes   = soup.find('ul', {'class' : 'productInfoInner' }).find_all('li') # find alle li tags der indeholder ul tags med klassen productInfoInner
    ingredients = getIngredients(boxes, 'Full ingredients list').text # find den "kasse" der indeholder ingredienserne

    print(brand, name, sign, price, ingredients, sep = ';') 
    print('\n')



products = getProducts('https://www.cultbeauty.co.uk/skin-care.html')  #  /products?loadedAmount=1980  # https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=1980&path=%2Fskin-care.html&parameters=%7B%7D

load_number = 30    
while ( load_number <= 2218 ):
    load_number += 30
    products = getProducts('https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=' + str(load_number) + '&path=%2Fskin-care.html&parameters=%7B%7D')  #  /products?loadedAmount=1980  # https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=1980&path=%2Fskin-care.html&parameters=%7B%7D
    print(len(products))
#print(products) # liste af produkt links
#print(len(products))

#for p in products:
#    print(getData(p))














