import json
import httplib2

class ODL_Controller:
    http = httplib2.Http()
    odl_ip = "10.15.3.19"
    odl_port = "6633"

    def __init__(self, ip, port):
        self.odl_ip = ip
        self.odl_port = port

    def getTopo(self):
            request_string = "http://"+self.odl_ip+":"+self.odl_port+"/controller/nb/v2/topology/default"     
            #request_string = "http://127.0.0.1:8181/restconf/operational/network-topology:network-topology/topology/topology-netconf/node/h1"
            resp, content = self.http.request(request_string, "GET")
            return content.decode()

odl0 = ODL_Controller("10.15.3.19", "8080")
print (odl0.getTopo())
