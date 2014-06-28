This folder contains the the programms for easy process chaining in PyWPS.
reciveXML.py and handlers.py has to be copied to the processes directory and recieveXML has to
be registerded in the __init__ file. Then it can be called as a PyWPS process with a XML describing 
the process chain as an input like in the example testXML.xml. If the processchain defined in testXML.xml
is used dummyprocess and dummyprocess2 has to be added to the processes directory. 
After the XML is called like this it is avaible as a PyWPS process with the defined inputs and outputs.
The programe manuellParser.py contains a commandline programm for translating the XML description dirctly
into an PyWPS process.