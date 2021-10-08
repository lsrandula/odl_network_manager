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
            resp, content = http.request(request_string, "GET")
            return content.decode()

odl0 = ODL_Controller("10.15.3.19", "6633")
print (odl0.getTopo())