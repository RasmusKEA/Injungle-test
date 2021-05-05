from bs4 import BeautifulSoup
import requests


def getBrands():
    base        = 'https://www.cultbeauty.co.uk'
    soup        = BeautifulSoup(requests.get(base + '/brands').text, 'html.parser')
    parent      = soup.find('ul', { 'class' : 'brandsList' })
    brands      = list(map(lambda n : base + n['href'].split('?')[0], parent.find_all('a', href = True)))
    return brands

def getProducts(link):
    base        = 'https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=0&path=%2Fskin-care.html&parameters=%7B%7D' # siden for hudpleje produkter
    soup        = BeautifulSoup(requests.get(link).text, 'html.parser') # html struktureres i soup objekt vha html parser
    parent      = soup.find('div', { 'class' : 'row' }) # div der indeholder alle produkter på siden
    print(parent)
    products    = list( map( lambda n : base + n['href'].split('#')[0], parent.find_all('a', href = True) ) ) # generer links til alle sidens produkter i en liste
    return products # returnerer listen med produkter


def getData(link):

    def getContent(items, text): #henter alle "kasserne" fra produkt siden
        for item in items:
            if item.find('div', {'class' : 'itemHeader'}).text.strip() == text.strip():
                return item.find('div', {'class' : 'itemContent'})
    
    def getDetails(node, tag, name):

        soup    = BeautifulSoup(requests.get(link).text, 'html.parser')

        brand   = getDetails(soup, 'div' , 'productBrandTitle'  )
        name    = getDetails(soup, 'div' , 'productTitle'       )
        size    = getDetails(soup, 'span', 'productSize'        )  
        sign    = getDetails(soup, 'span', 'productCurrency'    )
        price   = getDetails(soup, 'span', 'productPrice'       )

        
        boxes   = soup.find('ul', {'class' : 'productInfoInner' }).find_all('li')
        ingredients = getContent(boxes, 'Full ingredients list ').text

        print(brand, name, sign, price, ingredients, sep = ';') 
        print('\n')

load_number = 30    
if load_number < 60:#1959:
    load_number += 30
    products = getProducts('https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=' + str(load_number) + '&path=%2Fskin-care.html&parameters=%7B%7D')  #  /products?loadedAmount=1980  # https://www.cultbeauty.co.uk/xhr/partial/products?loadedAmount=1980&path=%2Fskin-care.html&parameters=%7B%7D
    print(len(products))

for p in products: 
    print(getData(p))













