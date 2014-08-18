#1111
from owslib.wps import WebProcessingService 
from pywps.Process import WPSProcess 
from owslib.wps import monitorExecution
import sys
from pywps import config
import time
class Process(WPSProcess): 
	def __init__(self): 
 		WPSProcess.__init__(self, identifier = 'example', title='Process Chain', version = '0.1',storeSupported = 'true', statusSupported = 'true', abstract='resulting process chain')
		self.Input1 = self.addLiteralInput(identifier= 'Input1' , title= 'first Input' ,default='5') 
		self.Input2 = self.addLiteralInput(identifier= 'Input2' , title= 'second Input' ,default='4') 
		self.Input3 = self.addLiteralInput(identifier= 'Input3' , title= 'third Input' ,default='6') 
		self.dummyprocess_1_output1 = self.addLiteralOutput(identifier= 'output1_dummyprocess_1' , title= 'output1')
		self.dummyprocess_2_output2 = self.addLiteralOutput(identifier= 'output2_dummyprocess_2' , title= 'output2')
		self.x = self.addLiteralOutput(identifier= 'x' , title= 'x')
	def execute(self):
		Outputs={}
		sys.stdout = open(config.getConfigValue("server","logFile"),'w') 
		try:
			wps = WebProcessingService('http://localhost/cgi-bin/pywps.cgi', verbose=True, skip_caps=True)
			identifier = 'dummyprocess' 
			description = wps.describeprocess(identifier)
			wps_outputs=[]
			for item in description.processOutputs:
				if item.dataType == 'ComplexOutput':
					wps_outputs.append((item.identifier, True))
				else: wps_outputs.append((item.identifier, False))
			inputs = [('i1',str(self.Input1.getValue())),('i2',str(self.Input2.getValue())),('i3',str(self.Input3.getValue()))]
			execution = wps.execute(identifier, inputs, output=wps_outputs)
			monitorExecution(execution)
			execution.checkStatus(sleepSecs=1)
			Outputs['dummyprocess_1']={}
			if "ComplexData" in description.processOutputs:
				i=0
				for output in execution.processOutputs:
					if description.processOutputs[i].dataType == 'ComplexData':
						Outputs['dummyprocess_1'][output.identifier]=output.reference 
					else: Outputs['dummyprocess_1'][output.identifier]=output.data[0] 
					i=i+1
			else:
				for output in execution.processOutputs:
					Outputs['dummyprocess_1'][output.identifier]=output.data[0] 
			x= Outputs['dummyprocess_1' ]['output1']
		except:
			wps = WebProcessingService('http://localhost/cgi-bin/pywps.cgi', verbose=True, skip_caps=True)
			identifier = 'dummyprocess' 
			description = wps.describeprocess(identifier)
			wps_outputs=[]
			for item in description.processOutputs:
				if item.dataType == 'ComplexOutput':
					wps_outputs.append((item.identifier, True))
				else: wps_outputs.append((item.identifier, False))
			inputs = [('i1',str(self.Input1.getValue())),('i2',str(self.Input2.getValue())),('i3',str(self.Input3.getValue()))]
			execution = wps.execute(identifier, inputs, output=wps_outputs)
			monitorExecution(execution)
			execution.checkStatus(sleepSecs=1)
			Outputs['dummyprocess_1']={}
			if "ComplexData" in description.processOutputs:
				i=0
				for output in execution.processOutputs:
					if description.processOutputs[i].dataType == 'ComplexData':
						Outputs['dummyprocess_1'][output.identifier]=output.reference 
					else: Outputs['dummyprocess_1'][output.identifier]=output.data[0] 
					i=i+1
			else:
				for output in execution.processOutputs:
					Outputs['dummyprocess_1'][output.identifier]=output.data[0] 
			x= Outputs['dummyprocess_1' ]['output1']
		try:
			wps = WebProcessingService('http://localhost/cgi-bin/pywps.cgi', verbose=True, skip_caps=True)
			identifier = 'dummyprocess' 
			description = wps.describeprocess(identifier)
			wps_outputs=[]
			for item in description.processOutputs:
				if item.dataType == 'ComplexOutput':
					wps_outputs.append((item.identifier, True))
				else: wps_outputs.append((item.identifier, False))
			inputs = [('i1',Outputs['dummyprocess_1']['output1']),('i2',x),('i3',Outputs['dummyprocess_1']['output2'])]
			execution = wps.execute(identifier, inputs)
			Outputs['dummyprocess_2']={}
			if "ComplexData" in description.processOutputs:
				i=0
				for output in execution.processOutputs:
					if description.processOutputs[i].dataType == 'ComplexData':
						Outputs['dummyprocess_2'][output.identifier]=output.reference 
					else: Outputs['dummyprocess_2'][output.identifier]=output.data[0] 
					i=i+1
			else:
				for output in execution.processOutputs:
					Outputs['dummyprocess_2'][output.identifier]=output.data[0] 
		except:
			wps = WebProcessingService('http://localhost/cgi-bin/pywps.cgi', verbose=True, skip_caps=True)
			identifier = 'dummyprocess' 
			description = wps.describeprocess(identifier)
			wps_outputs=[]
			for item in description.processOutputs:
				if item.dataType == 'ComplexOutput':
					wps_outputs.append((item.identifier, True))
				else: wps_outputs.append((item.identifier, False))
			inputs = [('i1',Outputs['dummyprocess_1']['output1']),('i2',x),('i3',Outputs['dummyprocess_1']['output2'])]
			execution = wps.execute(identifier, inputs)
			Outputs['dummyprocess_2']={}
			if "ComplexData" in description.processOutputs:
				i=0
				for output in execution.processOutputs:
					if description.processOutputs[i].dataType == 'ComplexData':
						Outputs['dummyprocess_2'][output.identifier]=output.reference 
					else: Outputs['dummyprocess_2'][output.identifier]=output.data[0] 
					i=i+1
			else:
				for output in execution.processOutputs:
					Outputs['dummyprocess_2'][output.identifier]=output.data[0] 
		self.dummyprocess_1_output1.setValue(Outputs['dummyprocess_1']['output1'])
		self.dummyprocess_2_output2.setValue(Outputs['dummyprocess_2']['output2'])
		self.x.setValue(x)
		sys.stdout.close()
		sys.stdout = sys.__stdout__
		return