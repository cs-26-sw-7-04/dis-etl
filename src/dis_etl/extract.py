from pygrametl.datasources import CSVSource

def csv_source(path) -> CSVSource:
    return CSVSource(f=open(path, "r", 16384), delimiter=';')


member_source      = csv_source('./data/member.csv')
product_source     = csv_source('./data/product.csv')
oldprice_source    = csv_source('./data/oldprice.csv')
sale_source         = csv_source('./data/sale.csv')
category_source     = csv_source('./data/category.csv')
product_categories_source = csv_source('./data/product_categories.csv')
room_source          = csv_source('./data/room.csv')
payment_source       = csv_source('./data/payment.csv')

for row in sale_source:
    print(row['id'], row['member_id'], row['product_id'], row['timestamp'], row['price'])