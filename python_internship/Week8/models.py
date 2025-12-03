# models.py
from db import get_connection
from utils import NotFoundError, ConflictError, logger

class User:
    def __init__(self, id=None, name=None, email=None):
        self.id = id
        self.name = name
        self.email = email

    @staticmethod
    def create(name, email):
        with get_connection() as conn:
            cur = conn.cursor()
            try:
                cur.execute("INSERT INTO users (name, email) VALUES (?, ?)", (name, email))
                user_id = cur.lastrowid
                logger.info(f"User created id={user_id}")
                return User.get_by_id(user_id)
            except Exception as e:
                # likely unique constraint
                logger.exception("Error creating user")
                raise ConflictError("Email already exists")

    @staticmethod
    def get_by_id(user_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            row = cur.fetchone()
            if not row:
                raise NotFoundError("User not found")
            return User(id=row["id"], name=row["name"], email=row["email"])

    @staticmethod
    def list_all():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM users")
            rows = cur.fetchall()
            return [User(id=r["id"], name=r["name"], email=r["email"]).__dict__ for r in rows]


class Product:
    def __init__(self, id=None, name=None, description=None, price=0.0, stock=0):
        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    @staticmethod
    def create(name, description, price, stock):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO products (name, description, price, stock) VALUES (?, ?, ?, ?)",
                (name, description, price, stock)
            )
            pid = cur.lastrowid
            logger.info(f"Product created id={pid}")
            return Product.get_by_id(pid)

    @staticmethod
    def get_by_id(product_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products WHERE id = ?", (product_id,))
            row = cur.fetchone()
            if not row:
                raise NotFoundError("Product not found")
            return Product(
                id=row["id"],
                name=row["name"],
                description=row["description"],
                price=row["price"],
                stock=row["stock"]
            )

    @staticmethod
    def list_all():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM products")
            rows = cur.fetchall()
            return [dict(r) for r in rows]

    def update(self, **kwargs):
        with get_connection() as conn:
            cur = conn.cursor()
            # simple update logic: only these fields allowed
            fields = []
            values = []
            for key in ("name", "description", "price", "stock"):
                if key in kwargs:
                    fields.append(f"{key} = ?")
                    values.append(kwargs[key])
            if not fields:
                return self
            values.append(self.id)
            sql = f"UPDATE products SET {', '.join(fields)} WHERE id = ?"
            cur.execute(sql, tuple(values))
            logger.info(f"Product updated id={self.id}")
            return Product.get_by_id(self.id)

    def delete(self):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("DELETE FROM products WHERE id = ?", (self.id,))
            logger.info(f"Product deleted id={self.id}")
            return True


class Order:
    def __init__(self, id=None, user_id=None, status='pending', total=0.0, created_at=None):
        self.id = id
        self.user_id = user_id
        self.status = status
        self.total = total
        self.created_at = created_at

    @staticmethod
    def create(user_id, items):
        """
        items: list of dicts: [{"product_id": int, "quantity": int}, ...]
        """
        with get_connection() as conn:
            cur = conn.cursor()
            # validate user exists
            cur.execute("SELECT id FROM users WHERE id = ?", (user_id,))
            if not cur.fetchone():
                raise NotFoundError("User not found")

            # calculate total and check stock
            total = 0
            for it in items:
                cur.execute("SELECT price, stock FROM products WHERE id = ?", (it["product_id"],))
                row = cur.fetchone()
                if not row:
                    raise NotFoundError(f"Product {it['product_id']} not found")
                if row["stock"] < it["quantity"]:
                    raise ConflictError(f"Insufficient stock for product {it['product_id']}")
                total += row["price"] * it["quantity"]

            # create order
            cur.execute("INSERT INTO orders (user_id, status, total) VALUES (?, ?, ?)", (user_id, 'placed', total))
            order_id = cur.lastrowid

            # create order items and reduce stock
            for it in items:
                cur.execute("SELECT price, stock FROM products WHERE id = ?", (it["product_id"],))
                row = cur.fetchone()
                price = row["price"]
                cur.execute(
                    "INSERT INTO order_items (order_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (order_id, it["product_id"], it["quantity"], price)
                )
                cur.execute("UPDATE products SET stock = stock - ? WHERE id = ?", (it["quantity"], it["product_id"]))

            logger.info(f"Order created id={order_id} total={total}")
            return Order.get_by_id(order_id)

    @staticmethod
    def get_by_id(order_id):
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
            row = cur.fetchone()
            if not row:
                raise NotFoundError("Order not found")
            order = Order(id=row["id"], user_id=row["user_id"], status=row["status"], total=row["total"], created_at=row["created_at"])
            # fetch items
            cur.execute("SELECT * FROM order_items WHERE order_id = ?", (order_id,))
            items = [dict(r) for r in cur.fetchall()]
            return {"order": order.__dict__, "items": items}

    @staticmethod
    def list_all():
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM orders")
            rows = cur.fetchall()
            return [dict(r) for r in rows]
