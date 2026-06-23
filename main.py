from datetime import datetime

# To produce non-damaging and corect values, we use escape function so that
# it automatically converts the special forbidden characters to the escaped version
from xml.sax.saxutils import escape
import xml.etree.ElementTree as ETree
from decimal import Decimal

CATEGORIES = [
    {
        "id": 2,
        "name": "Посуда",
        "is_active": True,
    },
    {
        "id": 1,
        "name": "Чай",
        "is_active": True,
    },
    {
        "id": 3,
        "name": "Подарочные наборы",
        "is_active": False,
    },
]


PRODUCTS = [
    {
        "id": 102,
        "name": "Чайник стеклянный",
        "slug": "glass-teapot",
        "category_id": 2,
        "price": "1500.00",
        "old_price": "1400.00",
        "stock": 0,
        "description": "Стеклянный чайник объёмом 800 мл",
        "image_url": "https://example.test/media/teapot-102.jpg",
        "is_active": True,
    },
    {
        "id": 101,
        "name": 'Чай "Лес & травы" <сбор №1>',
        "slug": "les-i-travy",
        "category_id": 1,
        "price": "490.00",
        "old_price": "590.00",
        "stock": 12,
        "description": "Вкус: мята & чабрец > классический чай",
        "image_url": "https://example.test/media/tea-101.jpg",
        "is_active": True,
    },
    {
        "id": 103,
        "name": "Скрытый товар",
        "slug": "hidden-product",
        "category_id": 1,
        "price": "350.00",
        "old_price": None,
        "stock": 5,
        "description": "Товар отключён администратором",
        "image_url": "https://example.test/media/product-103.jpg",
        "is_active": False,
    },
    {
        "id": 104,
        "name": "Пробник чая",
        "slug": "tea-sample",
        "category_id": 1,
        "price": "0.00",
        "old_price": None,
        "stock": 30,
        "description": "Бесплатный пробник",
        "image_url": "https://example.test/media/product-104.jpg",
        "is_active": True,
    },
    {
        "id": 105,
        "name": "Чашка фарфоровая",
        "slug": "porcelain-cup",
        "category_id": 2,
        "price": "700.00",
        "old_price": "900.00",
        "stock": 4,
        "description": "Фарфоровая чашка",
        "image_url": None,
        "is_active": True,
    },
    {
        "id": 106,
        "name": "Подарочный набор",
        "slug": "gift-set",
        "category_id": 3,
        "price": "2500.00",
        "old_price": "3000.00",
        "stock": 2,
        "description": "Товар находится в неактивной категории",
        "image_url": "https://example.test/media/product-106.jpg",
        "is_active": True,
    },
    {
        "id": 107,
        "name": "Чай улун молочный",
        "slug": "milk-oolong",
        "category_id": 1,
        "price": "700.50",
        "old_price": None,
        "stock": 3,
        "description": "",
        "image_url": "https://example.test/media/product-107.jpg",
        "is_active": True,
    },
]


def get_valid_products(products, active_category_ids):
    valid_products = []
    for product in products:
        # Here we are gonna check if the product or category bound to it is active or not
        if (
            not product["is_active"]
            or product["category_id"] not in active_category_ids
        ):
            continue
        product_name = product["name"]
        # here, whether the product name is in correct type, cause if it is in some type
        # other than string, it is logically fair to skip because product names are
        # usually in string type
        if not isinstance(product_name, str):
            continue
        # finally, we are checking if the product name is provided or not
        if product_name == "":
            continue
        if Decimal(product["price"]) <= 0:
            continue

        # Checking if the image url is provided and in correct format
        if isinstance(product["image_url"], str):
            if not (
                product["image_url"].startswith("https://")
                or product["image_url"].startswith("http://")
            ):
                continue
        else:
            continue
        valid_products.append(product)
    # Right before returning the results, we are sorting the products by their product
    # ids. Because key parameter in sorted() function takes not only key but also callable,
    # we can use that option to pass the product id inside each of the product dictionary
    # to the sorted function
    return sorted(valid_products, key=lambda product: product["id"])


def build_yml(products, categories, generated_at):
    # we wont be repeatedly iterating over categories
    # and check if they are active or not for each product
    # so it would prevent O(n^2) complexity
    # We will be using filter function to filter
    # out the active categories. Also, we are gonna sort the categories using
    # sorted() function similar to what we did for products in
    # get_valid_products function above. See the comment inside the function.
    active_categories = sorted(
        filter(lambda category: category["is_active"], categories),
        key=lambda category: category["id"],
    )
    active_category_ids = list(map(lambda item: item["id"], active_categories))
    valid_products = get_valid_products(products, active_category_ids)

    xml = '<?xml version="1.0" encoding="UTF-8"?>'
    # I'm using .strftime() here to format the date time in the expected format, seconds excluded.
    xml += f'<yml_catalog date="{generated_at.strftime('%Y-%m-%d %H:%M')}">'
    xml += "<shop>"

    xml += "<name>Test Shop</name>"
    xml += "<company>Test Company</company>"
    xml += "<url>https://example.test</url>"

    xml += '<currencies><currency id="RUB" rate="1"/></currencies>'

    xml += "<categories>"
    # By filtering out the active categories, we are completely eliminating
    # the need to use next() iterator function and do additional nested
    # for loop operations
    # for product in products:
    #     category = next(
    #         category
    #         for category in categories
    #         if category["id"] == product["category_id"]
    #     )
    for category in active_categories:
        xml += f'<category id="{category["id"]}">{escape(category["name"])}</category>'

    xml += "</categories>"
    xml += "<offers>"

    for product in valid_products:
        # Updated the attribute `available` so that it gives the correct values - true and false
        xml += '<offer id="{product_id}" available="{availability}">'.format(
            product_id=product["id"],
            availability="true" if product["stock"] > 0 else "false",
        )

        xml += (
            f"<url>"
            f'https://example.test/products/{escape(product["slug"])}/'
            f"</url>"
        )
        # Removing .replace() part to ensure period is used instead of comma
        # Using round function to only include 2 digits after period.
        price = round(Decimal(product["price"]))  # .replace(".", ",")

        xml += f"<price>{price}</price>"

        # Using < instead of <= to make sure the value is strictly greater than the current price
        # We are not checking if the old price and price values are greater than zero because we already did in get_valid_products fucntion
        if product["old_price"] and product["price"] < product["old_price"]:
            xml += f'<oldprice>{product["old_price"]}</oldprice>'

        xml += "<currencyId>RUB</currencyId>"
        xml += f'<categoryId>{product["category_id"]}</categoryId>'
        xml += f'<picture>{product["image_url"]}</picture>'
        xml += f'<name>{escape(product["name"])}</name>'
        # Skipping description tag inclusion if description is not provided
        if product["description"] or product["description"] is not None:
            xml += f'<description>{escape(product["description"])}</description>'
        xml += "</offer>"

    xml += "</offers>"
    xml += "</shop>"
    xml += "</yml_catalog>"

    return xml


if __name__ == "__main__":
    result = build_yml(
        products=PRODUCTS,
        categories=CATEGORIES,
        generated_at=datetime(year=2026, month=6, day=18, hour=12, minute=0),
    )

    with open("main.xml", "w") as file:
        file.write(result)
