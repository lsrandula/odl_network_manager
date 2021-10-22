import json
import httplib2
import requests
import xml.etree.ElementTree as ET

class ODL_Controller:
    http = httplib2.Http()

    def __init__(self, ip = "10.15.3.19", port = "6633", username = 'admin', password = 'admin'):
        self.odl_ip = ip
        self.odl_port = port
        self.ctrl_path = "http://" + self.odl_ip + ":" + self.odl_port
        self.username = username
        self.password = password

    # Get topology information from the controller
    def getTopo(self):
            get_topo = "/restconf/operational/network-topology:network-topology"
            URI = self.ctrl_path + get_topo
            headers = {'network-topology' : 'topology' ,'node' : 'node-id' , 'termination-point' : 'tp-id' }
            response = requests.get(URI, auth=(self.username, self.password), headers=headers)
            # string_xml =  response.json()
            # nodes = string_xml['network-topology']['topology'][0]['node'][0]
            nodes = response
            return nodes

    # Get flow statistics from the controller
    def getFlowStat(self):
            get_flowstat = "/restconf/operational/opendaylight-inventory:nodes/node/openflow:1/table/0/flow/fm-sr-link-discovery"
            URI = self.ctrl_path + get_flowstat
            response = requests.get(URI, auth=(self.username, self.password))
            # string_xml =  response.json()
            # nodes = string_xml['network-topology']['topology'][0]['node'][0]
            nodes = response


    # Add a flow to a switch
    def addFlow(self, datapath_id, flow_id):
        add_flow = "/restconf/config/opendaylight-inventory:nodes/node/" + datapath_id + "/table/0/flow/" + flow_id
        URI = self.ctrl_path + add_flow
        # r = requests.put(url, data=payload)

    # Delete a flow from a switch
    def deleteFlow(self, datapath_id, flow_id):
        delete_flow = "/restconf/config/opendaylightinventory:nodes/node/" + datapath_id + "/table/0/flow/"+ flow_id
        URI = self.ctrl_path + delete_flow

