# Author:	Jachym Cepicky
#        	http://les-ejk.cz
# Lince: 
# 
# Web Processing Service implementation
# Copyright (C) 2006 Jachym Cepicky
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301  USA


import subprocess
import wpsexceptions
from wpsexceptions import *
import time
import Inputs
import types

class Status:
    def __init__(self):
        self.creationTime = time.time()
        self.processAccepted = False
        self.processStarted = False
        self.processPaused = False
        self.processSucceeded = False
        self.processFailed = False

        self.processCompleted = 0
        self.exceptionReport = None


class Process:
    """
    """
    def __init__(self, identifier, title, abstract=None,
            metadata=[],profile=[], version=None,
            statusSupported=True, storeSupported=False):

        self.identifier = identifier
        self.version = version
        self.metadata = metadata
        self.title = title
        self.abstract = abstract
        self.wsdl  = None
        self.profile = profile
        self.storeSupported = storeSupported
        self.statusSupported = statusSupported

        self.status = Status()
        self.inputs = {}
        self.outputs = {}

    def addMetadata(self,Identifier, type, textContent):
        """Add new metadata to this process"""
        self.Metadata.append({
            "Identifier": Identifier,
            "type":type,
            "textContent":textContent})

    def addLiteralInput(self, identifier, title, abstract=None,
            uoms=None, minOccurs=1, maxOccurs=1, 
            allowedValues=("*"), type=types.IntType ,
            default=None, metadata= []):
        """
        Add new input item of type LiteralValue to this process
        """

        self.inputs[identifier] = Inputs.LiteralValue(identifier=identifier,
                title=title, abstract=abtract, metadata=metadata=[],
                minOccurs=minOccurs,maxOccurs=maxOccurs,
                type=type, uoms=uoms, values, default):

        return self.inputs[identifier]

    def addComplexInput(self,identifier,title,abtract=None,
                metadata=[],minOccurs=1,maxOccurs=1,
                formats=[],maxmegabites=0.1):

        self.inputs[identifier] = Inputs.ComplexInput(identifier=identifier,
                title=title,abtract=abstract,
                metadata=[],minOccurs=minOccurs,maxOccurs=maxOccurs,
                formats=formats, maxmegabites=maxmegabites)

        return self.inputs[identifier]


    def addBBoxInput(self,identifier,title,abtract=None,
                metadata=[],minOccurs=1,maxoccurs=1,
                crs=[]):
        self.inputs[identifier] = Inputs.BoundingBoxInput(self,
                identifier,title,abtract=abstract,
                metadata=metadata,minOccurs=minOccurs,maxOccurs=maxOccurs,
                crs=crs)

        return self.inputs[identifier]
 

    def AddLiteralOutput(self, Identifier, Title=None, Abstract=None,
            UOMs="m", value=None):
        """Add new output item of type LiteralValue to this process"""


        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        if not UOMs: 
            UOMs = "m"

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break
        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "LiteralValue": {"UOMs":UOMs,},
                            "value": value
                            })
        return self.Outputs[-1]


    def AddComplexOutput(self, Identifier, Title=None, Abstract=None,
            Formats=["text/xml"], Schemas=["http://schemas.opengis.net/gml/2.1.2/feature.xsd"], value=None):
        """Add new output item of type ComplexValue to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break

        if type(Formats) != type([]):
            Formats = [Formats]

        if type(Schemas) != type([]):
            Schemas = [Schemas]

        if (len(Formats) != len(Schemas)):
             self.failed = True
             raise ServerError("Number of Formats and Schemas does not match in process: %s" % self.Title)

        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "ComplexValue": {"Formats":Formats,"Schemas":Schemas},
                            "value": value
                            })

        return self.Outputs[-1]

    def AddComplexReferenceOutput(self, Identifier, Title=None, Abstract=None,
            Formats=["text/xml"], Schemas=["http://schemas.opengis.net/gml/2.1.2/feature.xsd"],value=None):
        """Add new output item of type ComplexValueValueReference to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break

        if type(Formats) != type([]):
            Formats = [Formats]

        if type(Schemas) != type([]):
            Schemas = [Schemas]

        if (len(Formats) != len(Schemas)):
             self.failed = True
             raise ServerError("Number of Formats and Schemas does not match in process: %s" % self.Title)

        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "ComplexValueReference": {"Formats":Formats,"Schemas":Schemas},
                            "value": value
                            })


    def AddBBoxOutput(self, Identifier, Title=None, Abstract=None, value=[]):
        """Add new output item of type BoundingBoxOutput to this process"""

        if not Title: 
            Title = ""

        if not Abstract: 
            Abstract = ""

        while 1:
            if self.GetOutput(Identifier):
                Identifier += "-1"
            else:
                break

        if len(value) < 4:
            for i in range(4-len(value)):
                value.append(0.0)

        self.Outputs.append({"Identifier":Identifier,"Title":Title,
                            "Abstract":Abstract,
                            "BoundingBoxValue": {},
                            "value": value
                            })

        return self.Outputs[-1]

    def GetInput(self,Identifier):
        """Returns input of defined identifier"""
        retinpt = None

        for inpt in self.Inputs:
            if inpt["Identifier"] == Identifier:
                retinpt = inpt
        return retinpt

    def GetOutput(self,Identifier):
        """Returns output of defined identifier"""
        retoupt = None

        for oupt in self.Outputs:
            if oupt["Identifier"] == Identifier:
                retoupt = oupt
        return retoupt

    def Cmd(self,cmd,stdin=None):
        """Runs command, fetches all messages and
        and sets self.status according to them, so
        the client application can track the progress information, when
        runing with Status=True

        This module is supposed to be used instead of 'os.system()', while
        running unix commands
        
        For GRASS modules, use GCmd(cmd)
        
        Example Usage:
            self.Cmd("gdalwarp -s_srs +init="epsg:4326" -t_srs \
            +init="esri:102067")

            output = self.Cmd("cs2cs  +proj=latlong +datum=NAD83\
                   +to  +proj=utm +zone=10 +datum=NAD27",
                    "45d15.551666667N   -111d30")
            """

    
        sys.stderr.write("PyWPS Cmd: %s\n" % (cmd.strip()))

        #cmd = string.split(cmd)
        try:
            p = subprocess.Popen(cmd,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,close_fds=True)
        except Exception,e :
            self.failed = True
            raise Exception("Could not perform command [%s]: %s" % (cmd,e))

        (stdout, stderr) = p.communicate(stdin)

        retcode = p.wait()

        if retcode != 0:
            self.failed = True
            sys.stderr.write("PyWPS stderr: %s\n" % (stderr))
            raise ServerError("Could not perform command: %s" % cmd)

        return stdout.splitlines()

    def SetStatus(self,message=None,percent=None):
        """Sets self.status variable according to given message and
        percents"""

        if self.status[1] == None:
            self.status[1] = 0

        if not message:
            message = self.status[0]

        if not percent:
            percent = self.status[1]

        try:
            percent = percent.replace("%","")
            precent = int(percent)
        except (AttributeError, ValueError):
            pass

        self.status = [message, percent]
        sys.stderr.write("PyWPS Status: %s\n" %message)

        return self.status

    def GetInputValue(self,Identifier):
        """Get value of selected input"""
        return self.GetInput(Identifier)["value"]

    def GetOutputValue(self,Identifier):
        """Get value of selected output"""
        return self.GetOutput(Identifier)["value"]

    def SetOutputValue(self,Identifier,value):
        """Set value of selected output"""
        out = self.GetOutput(Identifier)
        out["value"] = value

class GRASSWPSProcess(WPSProcess):
    """
    This class is to be used as base class for WPS processes in PyWPS
    script. To be able to use it's methods (functions), you have to start
    your process with following lines:

    from pywps.Wps.process import GRASSWPSProcess

    class Process(GRASSWPSProcess):
        def __init__(self):
            WPSProcess.__init__(self,
            Identifier="your_process_identifier",
            Title="Your process title",
            Abstract="Add optional abstract",
            storeSupported="true",
            grassLocation="/home/grass/spearfish60/",
            ...)

    Than you can add cusom process inputs and outputs:
            
            self.AddLiteralInput(Identifier="your_input_identifier",
                        Title="Your input title",
                        type=type(0), # integers only,
                        ...)

            self.AddComplexInput(Identifier="your_gml",
                        Title="Your gml input title",
                        ...)


    And you can ofcourse define your process outputs too:

            self.AddLiteralOutput(Identifier="output1",
                            Title="First output",
                            ...)
            self.AddComplexOutput(Identifier="gmlout",
                            Title="Embed GML",
                            ...)

    At the and, you can access the values of in- and outputs with help of
    GetInputValue and SetOutputValue methods:

        def execute(self):
            
            inputvalue = self.GetInputValue("your_input_identifier")
            inputGMLFile = self.GetInputValue("your_gml")

            self.SetOutputValue("output1", inputvalue)
            self.SetOutputValue("gmlout", inputGMLFile)

            return

    NOTE: Try to use self.Cmd("shell command") instead of os.system for
          GRASS modules. It will update your self.status report
          automatically.
          
          Try to use self.GCmd("g.module") as well, it will update
          self.status report based on percentage output from GRASS modules.


    """
    
    def __init__(self, Identifier, Title, processVersion="1.0", 
            Abstract="", statusSupported="false",
            storeSupported="false",grassLocation=None):

        WPSProcess.__init__(self,Identifier, Title,
                processVersion,Abstract,statusSupported,storeSupported)

        self.grassLocation = grassLocation

    def GCmd(self,cmd,stdin=None):
        """Runs GRASS command, fetches all GRASS_MESSAGE and
        GRASS_PERCENT messages and sets self.status according to them, so
        the client application can track the progress information, when
        runing with Status=True

        This module is supposed to be used instead of 'os.system()', while
        running GRASS modules
        
        Example Usage:
            self.Gcmd("r.los in=elevation.dem out=los coord=1000,1000")

            self.Gcmd("v.net.path network afcol=forward abcol=backward \
            out=mypath nlayer=1","1 9 12")
            """
        sys.stderr.write("PyWPS GCmd: %s\n" % (cmd.strip()))

        #cmd = string.split(cmd)
        try:
            p = subprocess.Popen(cmd,shell=True,
                stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,)
        except Exception,e :
            self.failed = True
            raise Exception("Could not perform command [%s]: %s" % (cmd,e))

        (stdout, stderr) = p.communicate(stdin)


        retcode = p.wait()

        if retcode != 0:
           self.failed = True
           sys.stderr.write("PyWPS stderr: %s\n" % (stderr))
           raise Exception("Could not perform command: %s" % cmd)

        return stdout.splitlines()
