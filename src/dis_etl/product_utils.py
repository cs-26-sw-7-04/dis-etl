from dis_etl.datetime_dim import get_datetime_key
from datetime import datetime as dt, timezone, timedelta

def get_history(source_row: dict, pricehistory) -> tuple[datetime, datetime, int, int]:
    relevanthistory = [row for row in pricehistory if row['product_id']==source_row["id"]]
    relevanthistory.sort(key=lambda r: r['changed_on'])

    output = []
    previous_change = dt.fromtimestamp(0, tz=timezone(timedelta(0)))
    i = 1
    for row in relevanthistory:
        output.append((previous_change, row['changed_on'], i, row['price']))
        previous_change = row['changed_on'];
        i+=1
    
    output.append((previous_change, dt.max.replace(tzinfo=timezone(timedelta(0))), i, source_row['price']))
        

    #print(f"Getting history of product {source_row['id']}. It has the times of {output}")
    return output



def decompose_product_row(source: dict, pricehistory) -> list:
    return [{
        "product_id": source["id"],
        "name": source["name"],
        "price": price/100,
        "alcohol_content_ml": source["alcohol_content_ml"],
        "active_state": "active" if source["active"] else "inactive",
        "category_major": "TEMPORARY",
        "category_minor": "TEMPORARY",
        "category_sub": "Temporary.",
        "category_subsub": "TEMPORARY!",
        "untildate": valid_to
    } for (valid_from, valid_to, version, price) in get_history(source, pricehistory)]