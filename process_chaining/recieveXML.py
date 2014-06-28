""" to do:
	Passwort fertig
	falls prozess schon vorhanden nicht nochmal in __init__.py eifnuegen
""" 

from pywps.Process import WPSProcess                                
from xml.sax import make_parser
from handlers import ProcessHandler
from pywps import config
import re

class Process(WPSProcess):
     def __init__(self):
          # init process
         WPSProcess.__init__(self,
              identifier = "recieveXML", # must be same, as filename
              title="parses xml",
              version = "0.1",
              storeSupported = "True",
              statusSupported = "True",
              abstract="chains processes")
              
         self.data = self.addComplexInput(identifier = "data",
                                            title = "Input file", 
					    formats=[{"mimeType":"application/xml"}])
	 self.password = self.addLiteralInput(identifier = "password", title="password")  
         self.output=self.addLiteralOutput(identifier="status", 
                                            title="status of process execution")
     def execute(self):
	 
	 process_path=config.getConfigValue("server","processesPath")
	 	 
	 ch = ProcessHandler()
	 saxparser = make_parser()
	 saxparser.setContentHandler(ch)
	 
	 input = file(self.data.getValue(), 'r')
	 filename = input.read()
	 input.close()
	 input = file(filename, 'r')
	 x = saxparser.parse(input)
	 outfile=process_path+str(ch.process_name)+".py"
	 output=file(outfile,'w')
	 
	 
	
	 output.write(ch.result)
	 output.close
         
	 init = file(process_path+"__init__.py",'r')
	 input = init.read()
	 input = re.sub('\n','',input)
	 input = re.sub(']','',input)
	 input += ",\""+ str(ch.process_name)+"\"]"
	 init = file(process_path+"__init__.py",'w')
	 init.write(input)
	 init.close()
	 self.output.setValue('successfully inserted '+ ch.process_name)
	 return
