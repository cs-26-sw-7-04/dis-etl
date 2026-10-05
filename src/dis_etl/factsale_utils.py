import csv
from datetime import datetime 

def fact_sale_grouped():
    with open('data/sale.csv', mode='r', encoding='utf-8') as f:
        reader= csv.DirtReader(f)
        rows = sorted(reader, key=lambda x: (x['member_id'], x['product_id'], x['timestamp_utc']))

    groupedsale = []

    prev_sale = None

    for current_sale in rows:
        current_sale_time = datetime.strptime(current_sale_row['timestamp_utc'], '%Y-%m-%d %H:%M:%S')

        if prev_sale is None: 
            current_sale['quantity'] = 1
            current_sale['price'] = int(current_sale['price'])
            groupedsale.append(current_sale)
            prev_sale = current_sale
            continue

        prev_sale_time = datetime.strptime(prev_sale['timestamp_utc'], '%Y-%m-%d %H:%M:%S')
        deltatime = (current_sale_time - prev_sale_time).total_seconds()

        if (current_sale['member_id'] == prev_sale['member_id'] and 
            current_sale['product_id'] == prev_sale['product_id'] and 
            deltatime <= 10):

            groupedsale[-1]['quantity'] += 1
            groupedsale[-1]['price'] = int(current_sale['price'])

        else:
            current_sale['quantity'] = 1
            current_sale['price'] = int(current_sale['price'])
            groupedsale.append(current_sale)
            prev_sale = current_sale

    return groupedsale



if __name__ == "__main__":
    fact_sale_quantity()

    