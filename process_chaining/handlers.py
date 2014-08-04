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
		self.wps_outputs=[]
		self.trye=False
		self.catch=False
		self.count_t=0 # count of additional tabstops
		self.synchron = True #execution modus, default is synchron
		self.sleepSecs= 1 # seconds to wait at asynchronus executions
		
	def startElement(self,name,attrs):
		if name == "workflow":
			self.process_name=attrs['identifier']
			self.result_head+="from owslib.wps import WebProcessingService \n"
			self.result_head+="from pywps.Process import WPSProcess \n"
			self.result_head+="from owslib.wps import monitorExecution\n"
			self.result_head+="import sys\n"
			self.result_head+="import time\n"
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
		
			
						
			
			if attrs['type']=="literal":
				self.inputs[attrs['localIdentifier']]=attrs['defaultValue']
				
				self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addLiteralInput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['title']+"\'"
	
				if "defaultValue" in attrs:
					self.result_head+=" ,default=\'"+ attrs['defaultValue']+"\'"
				self.result_head+=") \n"	
			if attrs['type'] == "complex":	
				self.inputs[attrs['localIdentifier']]=attrs['defaultValue']
				
				
				self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addComplexInput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['title']+"\',formats=[{\'mimeType\':\'"+attrs['mimeType']+"\'}])\n"
		
		if name == "try":
			self.trye = True
			
		if name == "catch":
			self.catch = True
			self.trye = False
		
		if name == "startProcess":
			self.activ.append(name)
			self.activ_process=attrs['processID']
			
			if self.trye == True:
				self.result_body+="\t\ttry:\n"
				self.count_t=1
			
			if self.catch == True:
				self.result_body+="\t\texcept:\n"
				self.count_t=1
			
			elif self.catch and self.trye == False:
				self.count_t=0
				
				
			self.result_body+=self.count_t*"\t"+"\t\twps = WebProcessingService(\'"+ attrs['service'] + "\', verbose=True, skip_caps=True)\n"
			self.result_body+=self.count_t*"\t"+"\t\tidentifier = \'" + attrs['identifier'] + "\' \n"
			
			#Get the outputs in order to build request
			self.result_body+=self.count_t*"\t"+"\t\tdescription = wps.describeprocess(identifier)\n"
			self.result_body+=self.count_t*"\t"+"\t\twps_outputs=[]\n"
			self.result_body+=self.count_t*"\t"+"\t\tfor item in description.processOutputs:\n"
			self.result_body+=self.count_t*"\t"+"\t\t\tif item.dataType == \'ComplexOutput\':\n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\twps_outputs.append((item.identifier, True))\n"
			self.result_body+=self.count_t*"\t"+"\t\t\telse: wps_outputs.append((item.identifier, False))\n"
		
			
			#synchron/asynchron process execution
			if 'synchron' in attrs:
				if attrs['synchron'] == 'True':	
					self.synchron = True
					#if 'sleepSecs' in attrs:
					self.sleepSecs=30 #attrs['sleepSecs']
						
				elif attrs['synchron'] == 'False':
					self.synchron = False
				
				
		if name == "input" and self.activ[-1] == "startProcess":
			
			if 'sourceIdentifier' in attrs:  
				self.process_inputs.append(("\'"+attrs['identifier']+"\'","str(self."+attrs['sourceIdentifier'] +".getValue())"))
			elif 'sourceProcess' in attrs:
				self.process_inputs.append(("\'"+attrs['identifier']+"\'", "Outputs[\'"+attrs['sourceProcess']+"\'][\'"+attrs['sourceName']+"\']"))
			else: self.process_inputs.append(("\'"+attrs['identifier']+"\'", attrs['localIdentifier']))	
		if name == "output" and self.activ[-1] == "startProcess":
			self.process_outputs.append([attrs['localIdentifier'],attrs['identifier']])
			
			#if attrs['type']=="literal":
				#self.wps_outputs.append("(\'"+attrs['identifier']+"\', False)")
			#if attrs['type']=="complex":
				#self.wps_outputs.append("(\'"+attrs['identifier']+"\', True)")
		if name == "outputs":
			self.activ.append(name)
		if name =="output" and self.activ[-1] == 'outputs':
			
			if "sourceProcess" in attrs:
				if attrs['type']=="literal":
					self.final_outputs.append("\t\tself."+attrs['sourceProcess']+"_"+attrs['sourceIdentifier']+".setValue(Outputs[\'"+attrs['sourceProcess']+"\'][\'"+attrs['sourceIdentifier']+"\'])\n" )
					self.result_head+="\t\tself."+attrs['sourceProcess']+'_' + attrs['sourceIdentifier'] +" = self.addLiteralOutput(identifier= \'" + attrs['sourceIdentifier'] + '_' + attrs['sourceProcess'] + "\' , title= \'" + attrs['sourceIdentifier']+"\')\n"
				elif attrs['type'] == "complex":
					self.final_outputs.append("\t\tself."+attrs['sourceProcess']+"_"+attrs['sourceIdentifier']+".setValue(Outputs[\'"+attrs['sourceProcess']+"\'][\'"+attrs['sourceIdentifier']+"\'])\n" )
					self.result_head+="\t\tself."+attrs['sourceProcess']+'_' + attrs['sourceIdentifier'] +" = self.addComplexOutput(identifier= \'" + attrs['sourceIdentifier'] + '_' + attrs['sourceProcess'] + "\' , title= \'" + attrs['sourceIdentifier']+"\')\n"	
			else: 
				if attrs['type'] == "literal":
					self.final_outputs.append("\t\tself."+attrs['localIdentifier']+".setValue("+attrs['localIdentifier']+")\n" )
					self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addLiteralOutput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['localIdentifier']+"\')\n"
	
				elif attrs['type'] =="complex":
					self.final_outputs.append("\t\tself."+attrs['localIdentifier']+".setValue("+attrs['localIdentifier']+")\n" )
					self.result_head+="\t\tself."+attrs['localIdentifier']+" = self.addComplexOutput(identifier= \'" + attrs['localIdentifier'] + "\' , title= \'" + attrs['localIdentifier']+"\')\n"	
	
	
		
			
	def endElement(self,name):
		if name == "inputs":
			x=self.activ.pop()
		if name == "outputs":
			x=self.activ.pop()
			self.result_head+="\tdef execute(self):\n"
			self.result_head+="\t\tOutputs={}\n"
			self.result_head+="\t\tsys.stdout = open('/tmp/wpsout.log','w') \n"
		
		if name == "try":
			self.trye = False
			self.count_t=0
			
		if name == "catch":
			self.catch = False
			self.count_t=0
		
		if name == "startProcess":
			x = self.activ.pop()
			
			
			#puts the inputs for the WPS request together
			self.result_body+=self.count_t*"\t"+"\t\tinputs = ["
			for item in self.process_inputs:
				self.result_body+="("+item[0]+","+item[1]+"),"
			self.process_inputs=[]
			self.result_body=self.result_body[:-1]
			self.result_body+="]\n"
			
			#builds the WPS request
			#Asynchronus request
			if self.synchron == False:
				self.result_body+=self.count_t*"\t"+"\t\texecution = wps.execute(identifier, inputs, output=wps_outputs)\n"
				self.result_body+=self.count_t*"\t"+"\t\tmonitorExecution(execution)\n"
				self.result_body+=self.count_t*"\t"+"\t\texecution.checkStatus(sleepSecs=" + str(self.sleepSecs) + ")\n"
				
			#Synchronus request
			elif self.synchron == True:
				self.result_body+=self.count_t*"\t"+"\t\texecution = wps.execute(identifier, inputs)\n"
			
			
			#process will be executet synchron by default
			self.synchron=True
			
			self.result_body+=self.count_t*"\t"+"\t\tOutputs[\'"+self.activ_process + "\']={}\n"
			
			#retrival of complex and literal output
			self.result_body+=self.count_t*"\t"+"\t\tif \"ComplexData\" in description.processOutputs:\n"
			self.result_body+=self.count_t*"\t"+"\t\t\ti=0\n"
			self.result_body+=self.count_t*"\t"+"\t\t\tfor output in execution.processOutputs:\n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\tif description.processOutputs[i].dataType == \'ComplexData\':\n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\t\tOutputs[\'"+ self.activ_process + "'][output.identifier]=output.reference \n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\telse: Outputs[\'"+ self.activ_process + "'][output.identifier]=output.data[0] \n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\ti=i+1\n"
			
			#retrival of literal output
			self.result_body+=self.count_t*"\t"+"\t\telse:\n"
			self.result_body+=self.count_t*"\t"+"\t\t\tfor output in execution.processOutputs:\n"
			self.result_body+=self.count_t*"\t"+"\t\t\t\tOutputs[\'"+ self.activ_process + "'][output.identifier]=output.data[0] \n"
			
			
			for item in self.process_outputs:
				self.result_body+=self.count_t*"\t"+"\t\t" + item[0] +"= Outputs[\'" + self.activ_process + "\' ][\'"+item[1]+ "\']\n"
			self.process_outputs=[]
	def endDocument(self):
		for item in self.final_outputs:
			self.result_tail+=item
		self.result_tail+="\t\tsys.stdout.close()\n"
		self.result_tail+="\t\tsys.stdout = sys.__stdout__\n"
		self.result_tail+="\t\treturn"
		
		self.result=self.result_head+self.result_body+self.result_tail
		
		
		
		
		
		
		
