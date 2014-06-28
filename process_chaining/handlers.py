"""to do: default value einfuegen"""
from xml.sax.handler import ContentHandler

class ProcessHandler(ContentHandler):
	def __init__(self):
		self.result_head = ""
		self.result_body = ""
		self.result_tail = ""
		self.result = ""
		self.activ = [] #contains open tags
		self.inputs={} #contains the inputs
		self.final_outputs=[]
		self.activ_process=""
		self.process_inputs=[]
		self.process_outputs=[]
		self.process_name=""
	def startElement(self,name,attrs):
		if name == "workflow":
			self.process_name=attrs['identifier']
			self.result_head+="from owslib.wps import WebProcessingService \n"
			self.result_head+="from owslib.wps import printInputOutput \n"
			self.result_head+="from pywps.Process import WPSProcess \n"
			self.result_head+="import sys\n"
			self.result_head+="class Process(WPSProcess): \n"
			self.result_head+="\tdef __init__(self): \n "
			self.result_head+="\t\tWPSProcess.__init__(self, "
			self.result_head+="identifier = \'"+ attrs['identifier']+"\', "
			self.result_head+="title=\'Process Chain\', "
			self.result_head+="version = \'0.1\',"
			self.result_head+="storeSupported = \'true\', "
			self.result_head+="statusSupported = \'true\', "
			self.result_head+="abstract=\'resulting process chain\')\n"
		if name == "inputs":
			self.activ.append(name)
		if name == "input" and self.activ[-1] == 'inputs':
			self.inputs[attrs['localIdentifier']]=attrs['defaultValue']
			self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addLiteralInput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['title']+"\')\n"
		if name == "startProcess":
			self.activ.append(name)
			self.activ_process=attrs['processID']
			self.result_body+="\t\twps = WebProcessingService(\'"+ attrs['service'] + "\', verbose=True, skip_caps=True)\n"
			self.result_body+="\t\tidentifier = \'" + attrs['identifier'] + "\' \n"
		if name == "input" and self.activ[-1] == "startProcess":
			
			if 'sourceIdentifier' in attrs:  
				self.process_inputs.append(("\'"+attrs['identifier']+"\'","str(self."+attrs['sourceIdentifier'] +".getValue())"))
			elif 'sourceProcess' in attrs:
				self.process_inputs.append(("\'"+attrs['identifier']+"\'", "Outputs[\'"+attrs['sourceProcess']+"\'][\'"+attrs['sourceName']+"\']"))
			else: self.process_inputs.append(("\'"+attrs['identifier']+"\'", attrs['localIdentifier']))	
		if name == "output" and self.activ[-1] == "startProcess":
			self.process_outputs.append([attrs['localIdentifier'],attrs['identifier']])
		if name == "outputs":
			self.activ.append(name)
		if name =="output" and self.activ[-1] == 'outputs':
			if "sourceProcess" in attrs:
				self.final_outputs.append("\t\tself."+attrs['sourceProcess']+"_"+attrs['sourceIdentifier']+".setValue(Outputs[\'"+attrs['sourceProcess']+"\'][\'"+attrs['sourceIdentifier']+"\'])\n" )
				self.result_head+="\t\tself."+attrs['sourceProcess']+'_' + attrs['sourceIdentifier'] +" = self.addLiteralOutput(identifier= \'" + attrs['sourceIdentifier'] + '_' + attrs['sourceProcess'] + "\' , title= \'" + attrs['sourceIdentifier']+"\')\n"
			else: 
				self.final_outputs.append("\t\tself."+attrs['localIdentifier']+".setValue("+attrs['localIdentifier']+")\n" )
				self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addLiteralOutput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['localIdentifier']+"\')\n"
	def endElement(self,name):
		if name == "inputs":
			x=self.activ.pop()
		if name == "outputs":
			x=self.activ.pop()
			self.result_head+="\tdef execute(self):\n"
			self.result_head+="\t\tOutputs={}\n"
			self.result_head+="\t\tsys.stdout = open('/tmp/wpsout.log','w') \n"
		if name == "startProcess":
			x = self.activ.pop()
			self.result_body+="\t\tinputs = ["
			for item in self.process_inputs:
				self.result_body+="("+item[0]+","+item[1]+"),"
			self.process_inputs=[]
			self.result_body=self.result_body[:-1]
			self.result_body+="]\n"
			self.result_body+="\t\texecution = wps.execute(identifier, inputs)\n"
			self.result_body+="\t\tOutputs[\'"+self.activ_process + "\']={}\n"
			self.result_body+="\t\tfor output in execution.processOutputs:\n"
			self.result_body+="\t\t\tOutputs[\'"+ self.activ_process + "'][output.identifier]=output.data[0] \n"
			for item in self.process_outputs:
				self.result_body+="\t\t" + item[0] +"= Outputs[\'" + self.activ_process + "\' ][\'"+item[1]+ "\']\n"
			self.process_outputs=[]
	def endDocument(self):
		for item in self.final_outputs:
			self.result_tail+=item
		self.result_tail+="\t\tsys.stdout.close()\n"
		self.result_tail+="\t\tsys.stdout = sys.__stdout__\n"
		self.result_tail+="\t\treturn"
		self.result=self.result_head+self.result_body+self.result_tail
		
		
		
		
		
		
		
