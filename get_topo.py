import json
import httplib2
import requests
import xml.etree.ElementTree as ET


class ODL_Controller:
    http = httplib2.Http()
    odl_ip = "10.15.3.19"
    odl_port = "6633"

    def __init__(self, ip, port):
        self.odl_ip = ip
        self.odl_port = port

    def getTopo(self):
            # request_string = "http://"+self.odl_ip+":"+self.odl_port+"/controller/nb/v2/topology/default"     
            #request_string = "http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/h1"
            # resp, content = self.http.request(request_string, "GET")
            # return content.decode()
            #request_string = "http://"+self.odl_ip+":"+self.odl_port+"/control>
            # request_string = "http://10.15.3.19:8181/restconf/operational/network-topology:network-topology"
            request_string = "http://" + self.odl_ip + ":" + self.odl_port + "/restconf/operational/network-topology:network-topology"
            #content = self.http.request(request_string, "GET")[1]
            headers = {'network-topology' : 'topology' ,'node' : 'node-id' , 'termination-point' : 'tp-id' }
            response = requests.get(request_string, auth=('admin', 'admin'), headers=headers)
            string_xml =  response.json()
            # json_string = string_xml.read()
            # json_data = json.loads(response.text)
            # xml_format = ET.fromstring(string_xml)
            # # testId = responseXml.find('data').find('testId')
            # return xml_format.text
            nodes = string_xml['network-topology']['topology'][0]['node'][0]

            # for i in nodes:
            #     print (i)
            # return 0

            return nodes

odl0 = ODL_Controller("10.15.3.19", "8181")
print (odl0.getTopo())
