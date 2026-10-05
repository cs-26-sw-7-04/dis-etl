import csv
from datetime import datetime 
from dis_etl.extract import get_sale_source

def fact_sale_grouped():
    
    rows = list(get_sale_source())
    rows.sort(key=lambda r: (int(r["member_id"]), int(r["product_id"]), r["timestamp"]))

    groupedsale = []
    prev_sale = None

    for current_sale in rows:

        if prev_sale is None: 
            current_sale["quantity"] = 1
            current_sale["price"] = int(current_sale["price"])
            groupedsale.append(current_sale)
            prev_sale = current_sale
            continue

        deltatime = (current_sale["timestamp"] - prev_sale["timestamp"]).total_seconds()

        if (current_sale["member_id"] == prev_sale["member_id"] and 
            current_sale["product_id"] == prev_sale["product_id"] and 
            deltatime <= 10):

            groupedsale[-1]["quantity"] += 1
            groupedsale[-1]["price"] = int(current_sale["price"])

        else:
            current_sale["quantity"] = 1
            current_sale["price"] = int(current_sale["price"])
            groupedsale.append(current_sale)
            prev_sale = current_sale

    return groupedsale



if __name__ == "__main__":
    print(fact_sale_grouped())

    