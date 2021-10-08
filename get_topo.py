import json
import httplib2

class ODL_Controller:
    self.http = httplib2.Http()
    self.odl_ip = "10.15.3.19"
    self.odl_port = "6633"

    def __init__(ip, port):
        self.odl_ip = ip
        self.odl_port = port

    def getTopo(self, h):
            request_string = "http://"+odl_ip+":"+odl_port_num+"/controller/nb/v2/topology/default"
            resp, content = http.request(request_string, "GET")
            return ODLObjDcontent.decode()ict

odl0 = ODL_Controller("10.15.3.19", "6633")
print (odl0.getTopo)