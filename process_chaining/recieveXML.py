from pywps.Process import WPSProcess                                
from xml.sax import make_parser
from handlers import ProcessHandler
from pywps import config
import re
import os.path

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
	 
	 #parsing of XML
	 ch = ProcessHandler()
	 saxparser = make_parser()
	 saxparser.setContentHandler(ch)
	 
	 input = file(self.data.getValue(), 'r')
	 filename = input.read()
	 input.close()
	 input = file(filename, 'r')
	 x = saxparser.parse(input)
	 
	 processpath=process_path+str(ch.process_name)+".py"
	 
	 #checks if process chain already exists. If it exists the password is
	 #ckecked and the process chain will be overwritten if the password is true.
	
	 if os.path.isfile(processpath):
	 	with open(processpath,'r') as f:
			password = f.readline()[1:].strip()
	 	if password == str(self.password.getValue()):
	 		output=file(processpath,'w')
	 		output.write('#'+str(self.password.getValue())+'\n'+ch.result)
	 		output.close
			message = 'successfully updated '+ ch.process_name
		else:
			message = 'you are not allowed to overwrite this process chain please choose a different name'
			
	 else:
		output=file(processpath,'w')
	 	output.write('#'+str(self.password.getValue())+'\n'+ch.result)
	 	output.close
			
         #updates the __init__.py file
	 	init = file(process_path+"__init__.py",'r')
	 	input = init.read()
	 	if ch.process_name in input:
	 		message = 'process already exists'
	 
	 	else:
	 		input = re.sub('\n','',input)
	 		input = re.sub(']','',input)
	 		input += ",\""+ str(ch.process_name)+"\"]"
	 		init = file(process_path+"__init__.py",'w')
	 		init.write(input)
	 		init.close()
			message = 'successfully inserted '+ ch.process_name
	 
	 self.output.setValue(message)
	 return
