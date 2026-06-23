# import xml.etree.ElementTree as ET

# tree = ET.Element("bitch")
# tree.text = "motherfucker"
# subElement = ET.SubElement(tree, "something")
# subElement.text = "I dont know"
# tree.append(subElement)


# print(ET.fromstring("<somethiung></somethiung>"))
# result = ET.parse("main.xml")

from xml.sax.saxutils import escape


print(escape('Чай "Лес & травы" <сбор №1>'))