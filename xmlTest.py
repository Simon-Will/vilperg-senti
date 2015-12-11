import xml.etree.cElementTree as ET

#HTML Datei holen??
root = ET.Element('product')
doc = ET.SubElement(root,'reviewList')
#subelm for each review?
ET.SubElement(doc, 'title', name = 'reviewTitle')
ET.SubElement(doc, 'text' , name = 'reviewText')
ET.SubElement(doc, 'numOfStars', name = 'stars')
ET.SubElement(doc, 'helpfulness', name = 'helpfulness')
ET.SubElement(doc, 'productId', name = 'id')
ET.SubElement(doc, 'date', name = 'date')

tree = ET.ElementTree(root)

tree.write('reviewList.xml')

print ET.tostring(root, pretty_print=True)
