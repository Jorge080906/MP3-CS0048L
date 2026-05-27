import datetime
import json
import os


class Product:
    def __init__(self, pid, name, price, stock):
        self.id = pid
        self.name = name
        self.price = price
        self.stock = stock


class Inventory:
    def __init__(self):
        self.products = {}
        self.history = []
        self.load_from_file()

    def save_to_file(self):
        serialized_products = {}

        for pid, p in self.products.items():
            serialized_products[pid] = {
                "id": p.id,
                "name": p.name,
                "price": p.price,
                "stock": p.stock
            }

        data_to_save = {
            "products": serialized_products,
            "history": self.history
        }

        with open("inventory.json", "w") as file:
            json.dump(data_to_save, file, indent=4)

    def load_from_file(self):
        if not os.path.exists("inventory.json"):
            return

        try:
            with open("inventory.json", "r") as file:
                data = json.load(file)

                self.history = data.get("history", [])
                saved_products = data.get("products", {})

                for pid, p_info in saved_products.items():
                    self.products[pid] = Product(
                        pid=p_info["id"],
                        name=p_info["name"],
                        price=p_info["price"],
                        stock=p_info["stock"]
                    )

        except (json.JSONDecodeError, KeyError):
            print("Error reading database file.")

    def log_transaction(self, message):
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history.append(f"[{timestamp}] {message}")

    def add_product(self, pid, name, price, stock):
        if pid in self.products:
            return "Product ID already exists."

        self.products[pid] = Product(pid, name, price, stock)

        self.log_transaction(
            f"Added Product: {name} (ID: {pid}, Qty: {stock})"
        )

        self.save_to_file()

        return "Product added successfully."

    def update_product(self, pid, name=None, price=None, stock=None):
        if pid not in self.products:
            return "Product not found."

        product = self.products[pid]

        changes = []

        if name:
            changes.append(f"Name from '{product.name}' to '{name}'")
            product.name = name

        if price is not None:
            changes.append(f"Price from {product.price} to {price}")
            product.price = price

        if stock is not None:
            changes.append(f"Stock from {product.stock} to {stock}")
            product.stock = stock

        if changes:
            self.log_transaction(
                f"Updated Product ID {pid}: " + ", ".join(changes)
            )

            self.save_to_file()

        return "Product updated successfully."

    def record_sale(self, pid, quantity):
        if pid not in self.products:
            return "Product not found."

        product = self.products[pid]

        if product.stock < quantity:
            return "Not enough stock."

        product.stock -= quantity

        total = product.price * quantity

        self.log_transaction(
            f"Sale: {product.name} (ID: {pid}, Qty: {quantity}) Total: ${total:.2f}"
        )

        self.save_to_file()

        return f"Sale recorded. Total: ${total:.2f}"

    def low_stock_alert(self, threshold=5):
        alerts = []

        for p in self.products.values():
            if p.stock <= threshold:
                alerts.append(
                    f"{p.name} (ID: {p.id}) low stock: {p.stock}"
                )

        return alerts if alerts else ["No low stock items."]

    def calculate_total_value(self):
        total_val = sum(
            p.price * p.stock for p in self.products.values()
        )

        return total_val

    def search_products(self, query):
        results = []

        query = query.lower()

        for p in self.products.values():
            if query == p.id.lower() or query in p.name.lower():
                results.append(p)

        return results

    def display_products(self):
        if not self.products:
            print("No products available.")
            return

        for p in self.products.values():
            print(
                f"ID: {p.id}, Name: {p.name}, Price: {p.price}, Stock: {p.stock}"
            )

    def display_history(self):
        if not self.history:
            print("No transactions recorded yet.")
            return

        for record in self.history:
            print(record)


def load_accounts():
    if not os.path.exists("accounts.json"):
        default_account = {
            "admin": "password"
        }

        with open("accounts.json", "w") as file:
            json.dump(default_account, file, indent=4)

    with open("accounts.json", "r") as file:
        return json.load(file)


def save_accounts(accounts):
    with open("accounts.json", "w") as file:
        json.dump(accounts, file, indent=4)


def create_account():
    accounts = load_accounts()

    print("\n====== Create Account ======")

    username = input("Enter new username: ")

    if username in accounts:
        print("Username already exists.")
        return

    password = input("Enter new password: ")

    accounts[username] = password

    save_accounts(accounts)

    print("Account created successfully!")


def authenticate():
    accounts = load_accounts()

    print("\n====== Login ======")

    attempts = 3

    while attempts > 0:
        username = input("Username: ")
        password = input("Password: ")

        if username in accounts and accounts[username] == password:
            print("Login successful!\n")
            return True

        attempts -= 1

        print(f"Incorrect credentials. Attempts remaining: {attempts}")

    return False


def inventory_menu(inv):
    while True:
        print("\n====== Main Menu ======")
        print("1 Add Product")
        print("2 Update Product")
        print("3 Record Sale")
        print("4 Show All Products")
        print("5 Low Stock Alerts")
        print("6 Calculate Total Inventory Value")
        print("7 Search Products")
        print("8 View Sales History")
        print("9 Log Out")

        choice = input("Enter choice: ")

        if choice == '1':
            pid = input("ID: ")
            name = input("Name: ")

            try:
                price = float(input("Price: "))
                stock = int(input("Stock: "))

                print(inv.add_product(pid, name, price, stock))

            except ValueError:
                print("Invalid price or stock input.")

        elif choice == '2':
            pid = input("ID: ")

            name = input("New name (leave blank to skip): ")
            price_input = input("New price (leave blank to skip): ")
            stock_input = input("New stock (leave blank to skip): ")

            try:
                price = float(price_input) if price_input else None
                stock = int(stock_input) if stock_input else None

                print(
                    inv.update_product(
                        pid,
                        name if name else None,
                        price,
                        stock
                    )
                )

            except ValueError:
                print("Invalid price or stock input.")

        elif choice == '3':
            pid = input("ID: ")

            try:
                quantity = int(input("Quantity: "))

                print(inv.record_sale(pid, quantity))

            except ValueError:
                print("Invalid quantity.")

        elif choice == '4':
            inv.display_products()

        elif choice == '5':
            try:
                thresh_input = input(
                    "Enter threshold (default 5): "
                )

                thresh = int(thresh_input) if thresh_input else 5

                alerts = inv.low_stock_alert(thresh)

            except ValueError:
                print("Invalid input. Using default of 5.")
                alerts = inv.low_stock_alert()

            for alert in alerts:
                print(alert)

        elif choice == '6':
            total = inv.calculate_total_value()

            print(f"Total Inventory Value: ${total:.2f}")

        elif choice == '7':
            query = input("Search Product ID or Name: ")

            results = inv.search_products(query)

            if not results:
                print("No products found.")

            for p in results:
                print(
                    f"Found > ID: {p.id}, Name: {p.name}, Price: {p.price}, Stock: {p.stock}"
                )

        elif choice == '8':
            inv.display_history()

        elif choice == '9':
            print("Logging out...")
            break

        else:
            print("Invalid choice.")


def main():
    while True:
        print("\n====== Inventory System ======")
        print("1 Login")
        print("2 Create Account")
        print("3 Exit")

        start_choice = input("Enter choice: ")

        if start_choice == '1':

            if authenticate():
                inv = Inventory()
                inventory_menu(inv)

            else:
                print("Access denied.")

        elif start_choice == '2':
            create_account()

        elif start_choice == '3':
            print("Exiting system...")
            break

        else:
            print("Invalid choice.")


if __name__ == "__main__":
    main()
