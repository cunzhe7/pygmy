class Book:
    id_book = None
    name = None
    category = None
    price = None 
    stock = None

    def __init__(self, id_book,name, category, price, stock):
        self.id_book = id_book
        self.name = name
        self.category = category
        self.price =  price
        self.stock = stock
