# services.py
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from models import Product
from utils import logger, APIError

def product_from_row(row):
    # row is dict from csv DictReader
    name = row.get("name")
    if not name:
        raise APIError("Product name missing")
    description = row.get("description", "")
    try:
        price = float(row.get("price", 0))
    except:
        price = 0.0
    try:
        stock = int(float(row.get("stock", 0)))
    except:
        stock = 0
    return {"name": name, "description": description, "price": price, "stock": stock}

def read_csv_stream(file_stream):
    """
    Generator to yield rows from CSV file stream (decoding handled by Flask)
    """
    file_stream.seek(0)
    text = file_stream.read().decode('utf-8').splitlines()
    reader = csv.DictReader(text)
    for row in reader:
        yield row

def create_product_worker(row):
    try:
        pdata = product_from_row(row)
        p = Product.create(**pdata)
        logger.info(f"Bulk created product id={p.id} name={p.name}")
        return {"status": "success", "product_id": p.id}
    except Exception as e:
        logger.exception("Error in product worker")
        return {"status": "error", "error": str(e), "row": row}

def bulk_upload_products(file_stream, max_workers=5):
    """
    Uses threads to process each CSV row concurrently.
    Returns list of results.
    """
    rows = list(read_csv_stream(file_stream))
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(create_product_worker, r) for r in rows]
        for fut in as_completed(futures):
            results.append(fut.result())
    return results
