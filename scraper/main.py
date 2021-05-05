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

products = db.child("products").order_by_child(
    "name").equal_to("Niacinamide").get()
for product in products.each():
    if (product.val()['brand'] == "THE INKEY LIST"):
        print("ja nice")
