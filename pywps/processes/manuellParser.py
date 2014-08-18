from handlers import ProcessHandler
from xml.sax import make_parser
from lxml import etree
import sys
from pywps import config

xml_doc=sys.argv[1]	 
output=file(sys.argv[2],'w')

#validation of the XML
xmlname = file(xml_doc, 'r')
schema=file('process_chain.xsd')
xmlschema_doc=etree.parse(schema)
xmlschema = etree.XMLSchema(xmlschema_doc)

xml = etree.parse(xmlname)
validate = xmlschema.validate(xml)

#Parsing of the XML
if validate == True:
	ch = ProcessHandler()
	saxparser = make_parser()
	saxparser.setContentHandler(ch)
	filename = file(xml_doc, 'r')
	x = saxparser.parse(filename)

	output.write(ch.result)
	output.close

else: print 'XML not valid'
