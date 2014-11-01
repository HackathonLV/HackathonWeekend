################### websiteBeta/productXMLHandler.py ####################
#########################################################################
# The product XML handler class is designed to read barcodes from
# passed in XML files, look up the values for a product based on
# that barcode, then create an XML file with that information in
# it. The Product XML Handler should also be able to read this
# information and return it.
#########################################################################

from xml.etree import ElementTree as ET
import os

class productXMLHandler():
    # Static class variables (for storage/remembering stuff)
    currentBarcodeNumber = 0
    currentProductName = ""
    currentProductImage = ""
    currentProductPrice = ""
    # temp location for XML storage while debugging
    XML_STORAGE_PATH = "C:\\Users\\Boler\\Desktop\\xml test location\\productInformation.xml"

    def __init__(self):
        placeholder = "placeholder"

    def lookupBarcode(self, barcodeXML):
        # Simple error checking, make sure the XML exists
        if not os.path.exists(barcodeXML):
            return False

        # Make sure the XML file is, indeed, and XML file
        if ".xml" not in barcodeXML.lower():
            return False

        # If the XML exists, parse it and try to pull the barcode from it
        tree = ET.parse(barcodeXML)
        rootBarcodeXML = tree.getroot()

        # Clean the previous barcode lookup for error handling
        self.currentBarcodeNumber = 0

        # Read the tag
        for item in rootBarcodeXML:
            if item.tag == "item":
                self.currentBarcodeNumber = item.attrib["id"]

        # Return the barcode number
        return self.currentBarcodeNumber

    def lookupProductInformation(self, barcodeNumber):
        # <item name="productName" image="imagePath.png" price="9.99"></item>
        # Hard coded dictionary for current barcode information (proof of concept)
        productDictionary = {"0938098321" : {'name' : "productName", "image" : "imagePath.png", "price" : "9.99"}}
        xmlIndent = "    "

        # Check that the passed in barcode number exists in the database dictionary
        if barcodeNumber not in productDictionary:
            return False

        # If the barcode exists in the data, create the XML
        XMLWriteList = []
        XMLWriteList.append('<data>')
        XMLWriteList.append(xmlIndent + '<item name="%s" image="%s" price="%s"></item>'
                            % (productDictionary[barcodeNumber]["name"],
                               productDictionary[barcodeNumber]["image"],
                               productDictionary[barcodeNumber]["price"]))
        XMLWriteList.append('</data>')

        # Write out the XML file
        productXMLFile = open(self.XML_STORAGE_PATH, 'w+')
        for line in XMLWriteList:
            productXMLFile.write(line + "\n")

        productXMLFile.close()

    # Stores the product information into the class, so it can be referenced
    def getProductInfoFromXML(self, productXML):
        # Verify the XML file exists
        if not os.path.exists(productXML) or ".xml" not in productXML.lower():
            return False

        # Parse the XML file into an element tree
        tree = ET.parse(productXML)
        rootProductXML = tree.getroot()

        # Clean up the previously stored product info to prevent mix up issues
        self.currentProductName = ""
        self.currentProductImage = ""
        self.currentProductPrice = ""

        # Parse the XML file
        for item in rootProductXML:
            if item.tag == "item":
                self.currentProductName = item.attrib["name"]
                self.currentProductImage = item.attrib["image"]
                self.currentProductPrice = item.attrib["price"]

# __MAIN METHOD FOR TESTING__ #
XMLHandlerTest = productXMLHandler()

theBarcode = XMLHandlerTest.lookupBarcode("C:\\Users\\Boler\\Documents\\GitHub\\HackathonWeekend\\ExpressLane\\sampleData.xml")
print XMLHandlerTest.currentBarcodeNumber
XMLHandlerTest.lookupProductInformation(theBarcode)
XMLHandlerTest.getProductInfoFromXML(XMLHandlerTest.XML_STORAGE_PATH)
print XMLHandlerTest.currentProductName
print XMLHandlerTest.currentProductImage
print XMLHandlerTest.currentProductPrice