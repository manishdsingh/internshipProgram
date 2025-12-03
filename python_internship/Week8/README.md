python -m venv myenv
myenv\Scripts\activate
pip install flask
python app.py init-db
python app.py run

Server runs at: http://127.0.0.1:5000/



Step 1: Health Check

Request:

GET http://127.0.0.1:5000/health


Output:

{
  "status": "ok"
}
<!-- ___________________________ -->
Step 2: Test Users API
2a. Create User

Request:

POST http://127.0.0.1:5000/users
Content-Type: application/json
Body:
{
    "name": "Alice",
    "email": "alice@example.com"
}


Expected Output:

{
    "user": {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }
}
<!-- ______________________________________ -->
2b. List Users

Request:

GET http://127.0.0.1:5000/users


Expected Output:

{
    "users": [
        {
            "id": 1,
            "name": "Alice",
            "email": "alice@example.com"
        }
    ]
}
<!-- ______________________________ -->
2c. Get Single User

Request:

GET http://127.0.0.1:5000/users/1


Expected Output:

{
    "user": {
        "id": 1,
        "name": "Alice",
        "email": "alice@example.com"
    }
}
<!-- ________________________ -->
Step 3: Test Products API
3a. Create Product

Request:

POST http://127.0.0.1:5000/products
Content-Type: application/json
Body:
{
    "name": "Laptop",
    "description": "Gaming Laptop",
    "price": 1200,
    "stock": 5
}


Expected Output:

{
    "product": {
        "id": 1,
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1200.0,
        "stock": 5
    }
}
<!-- __________________________ -->
b. List Products

Request:

GET http://127.0.0.1:5000/products


Expected Output:

{
    "products": [
        {
            "id": 1,
            "name": "Laptop",
            "description": "Gaming Laptop",
            "price": 1200.0,
            "stock": 5
        }
    ]
}
<!-- _____________________ -->
3d. Update Product

Request:

PUT http://127.0.0.1:5000/products/1
Content-Type: application/json
Body:
{
    "stock": 10,
    "price": 1100
}


Expected Output:

{
    "product": {
        "id": 1,
        "name": "Laptop",
        "description": "Gaming Laptop",
        "price": 1100.0,
        "stock": 10
    }
}
<!-- __________________ -->
3e. Delete Product

Request:

DELETE http://127.0.0.1:5000/products/1


Expected Output:

{
    "deleted": true
}
<!-- _________________ -->
3f. Bulk Upload Products (CSV)

CSV Example (products.csv):

name,description,price,stock
Mouse,Wireless Mouse,20,50
Keyboard,Mechanical Keyboard,80,30


Request:

POST http://127.0.0.1:5000/products/bulk-upload
Form-Data:
file = products.csv


Expected Output:

{
    "results": [
        {"status": "success", "product_id": 2},
        {"status": "success", "product_id": 3}
    ]
}
<!-- ____________________________ -->

