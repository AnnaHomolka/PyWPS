from handlers import ProcessHandler
from xml.sax import make_parser
ch = ProcessHandler()
saxparser = make_parser()
saxparser.setContentHandler(ch)
	 
output=file('xyztest.py','w')
filename = file('/home/user/shared/testXML.xml', 'r')
#filename = input.read()
#input.close()
#input = file(filename, 'r')
#data = input.read()
x = saxparser.parse(filename)
output.write(ch.result)
output.close
