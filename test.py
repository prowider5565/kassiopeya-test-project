# import xml.etree.ElementTree as ET

# tree = ET.Element("bitch")
# tree.text = "motherfucker"
# subElement = ET.SubElement(tree, "something")
# subElement.text = "I dont know"
# tree.append(subElement)


# print(ET.fromstring("<somethiung></somethiung>"))
# result = ET.parse("main.xml")

# from xml.sax.saxutils import escape


# print(escape('Чай "Лес & травы" <сбор №1>'))

# CATEGORIES = [
#     {
#         "id": 1,
#         "name": "Чай",
#         "is_active": True,
#     },
#     {
#         "id": 2,
#         "name": "Посуда",
#         "is_active": True,
#     },
#     {
#         "id": 3,
#         "name": "Подарочные наборы",
#         "is_active": False,
#     },
# ]



# active_categories = filter(lambda category: category["is_active"], CATEGORIES)

# print(list(active_categories))
# from decimal import Decimal

# print(Decimal("4.5") > Decimal("34.5"))

# print(round(Decimal("23.45543"), ndigits=2))