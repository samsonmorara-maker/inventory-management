import requests
BASE_URL = "http://127.0.0.1:5000"
def view_inventory():
    try:
        response = requests.get(
            f"{BASE_URL}/inventory"
        )
        if response.status_code == 200:
            products = response.json()
            if not products:
                print("Inventory is empty")
                return
            for product in products:
                print("\n----------------")
                print(f"ID: {product['id']}")
                print(f"Name: {product['product_name']}")
                print(f"Brand: {product['brands']}")
                print(f"Quantity: {product['quantity']}")
                print(f"Price: ${product['price']}")
        else:
            print("Could not load inventory")
    except requests.exceptions.ConnectionError:
        print("Cannot connect to Flask API")

def view_product():
    try:
        product_id = int(
            input("Enter product ID: ")
        )
    except ValueError:
        print("ID must be a number")
        return
    response = requests.get(
        f"{BASE_URL}/inventory/{product_id}"
    )

    if response.status_code == 200:
        print(response.json())
    else:
        print("Product not found")

def add_product():
    barcode = input(
        "Barcode: "
    )

    try:
        quantity = int(
            input("Quantity: ")
        )
        price = float(
            input("Price: ")
        )
    except ValueError:
        print("Quantity and price must be numbers")
        return
    data = {
        "barcode": barcode,
        "quantity": quantity,
        "price": price
    }
    response = requests.post(
        f"{BASE_URL}/inventory",
        json=data
    )
    if response.status_code == 201:
        print("Product added")
        print(response.json())
    else:
        print(response.json())

def update_product():
    try:
        product_id = int(
            input("Product ID: ")
        )
    except ValueError:
        print("Invalid ID")
        return

    print("""
1. Update price
2. Update quantity
""")


    choice = input(
        "Choice: "
    )

    if choice == "1":
        try:
            price = float(
                input("New price: ")
            )

        except ValueError:
            print("Invalid price")
            return


        data = {
            "price": price
        }
    elif choice == "2":
        try:
            quantity = int(
                input("New quantity: ")
            )
        except ValueError:
            print("Invalid quantity")
            return
        data = {
            "quantity": quantity
        }
    else:
        print("Invalid choice")
        return
    response = requests.patch(
        f"{BASE_URL}/inventory/{product_id}",
        json=data
    )

    if response.status_code == 200:
        print("Updated successfully")
    else:
        print(response.json())

def delete_product():
    try:
        product_id = int(
            input("Product ID: ")
        )
    except ValueError:
        print("Invalid ID")
        return
    response = requests.delete(
        f"{BASE_URL}/inventory/{product_id}"
    )
    if response.status_code == 200:
        print("Product deleted")
    else:
        print(response.json())

def find_product():
    barcode = input(
        "Enter barcode: "
    )
    response = requests.get(
        f"{BASE_URL}/products/barcode/{barcode}"
    )
    if response.status_code == 200:
        print("\nProduct found:")
        print(response.json())
    else:
        print("Product not found")

def menu():
    while True:
        print("""
======== Inventory Manager ========

1. View inventory
2. View product
3. Add product
4. Update product
5. Delete product
6. Find product from OpenFoodFacts
7. Exit

===================================
""")
        choice = input(
            "Select option: "
        )
        if choice == "1":
            view_inventory()
        elif choice == "2":
            view_product()
        elif choice == "3":
            add_product()
        elif choice == "4":
            update_product()
        elif choice == "5":
            delete_product()
        elif choice == "6":
            find_product()
        elif choice == "7":
            print("Goodbye")
            break
        else:
            print("Invalid option")
if __name__ == "__main__":
    menu()