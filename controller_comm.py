# Handles communication with the OpenDayLight controller

import json
import httplib2
import requests
import xml.etree.ElementTree as ET

class ODL_Controller:
    http = httplib2.Http()

    def __init__(self, ip = "10.15.3.19", port = "8181", username = 'admin', password = 'admin'):
        self.odl_ip = ip
        self.odl_port = port
        self.ctrl_path = "http://" + self.odl_ip + ":" + self.odl_port
        self.username = username
        self.password = password

    # Get topology information from the controller
    def getTopo(self):
            # get_topo = "/restconf/operational/network-topology:network-topology"
            get_topo = "/restconf/operational/network-topology:network-topology/topology/flow:1"
            URI = self.ctrl_path + get_topo
            print (URI)
            # headers = {'network-topology' : 'topology' ,'node' : 'node-id' , 'termination-point' : 'tp-id' }
            response = requests.get(URI, auth=(self.username, self.password))
            # response = requests.get(URI, auth=(self.username, self.password), headers=headers)
            string_xml =  response.json()
            nodes = []
            links = []
            for i in range(len(string_xml['topology'][0]['node'])):
                nodes.append(string_xml['topology'][0]['node'][i]['node-id'])
            for i in range(len(string_xml['topology'][0]['link'])):
                links.append(string_xml['topology'][0]['link'][i]['link-id'])
            return nodes,links

    # Get flow statistics from the controller for the switch given by "datapath_id"
    def getFlowStat(self, datapath_id):
            get_flowstat = "/restconf/operational/opendaylight-inventory:nodes/node/"
            URI = self.ctrl_path + get_flowstat + datapath_id
            response = requests.get(URI, auth=(self.username, self.password))
            string_xml =  response.json()
            flows = []
            flow_entries = []
            for i in range(len(string_xml['node'][0]['flow-node-inventory:table'])):
                if (string_xml['node'][0]['flow-node-inventory:table'][i]['id'] == 0):
                    flows = string_xml['node'][0]['flow-node-inventory:table'][i]['flow']
                    break
            for i in range(len(flows)):
                id = flows[i]['id']
                priority = flows[i]['priority']
                cookie = flows[i]['cookie']
                match = flows[i]['match']
                idle_timeout = flows[i]['idle-timeout']
                hard_timeout = flows[i]['hard-timeout']
                flow_entry = [cookie, priority, match, idle_timeout, hard_timeout]
                flow_entries.append(flow_entry)
            return flow_entries
            
    # Add a flow to a switch
    def addFlow(self, datapath_id, flow_id):
        add_flow = "/restconf/operations/sal-flow:add-flow"
        URI = self.ctrl_path + add_flow
        # r = requests.put(url, data=payload)

    # Delete a flow from a switch
    def deleteFlow(self, datapath_id, flow_id):
        delete_flow = "/restconf/operations/sal-flow:remove-flow"
        URI = self.ctrl_path + delete_flow

