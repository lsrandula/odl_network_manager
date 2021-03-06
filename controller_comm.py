# Handles communication with the OpenDayLight controller

import json
import httplib2
import requests
import xml.etree.ElementTree as ET

class ODL_Controller:
    http = httplib2.Http()

    def __init__(self, ip = "192.168.1.6", port = "8181", username = 'admin', password = 'admin'):
        self.odl_ip = ip
        self.odl_port = port
        self.ctrl_path = "http://" + self.odl_ip + ":" + self.odl_port
        self.username = username
        self.password = password

    # Get topology information from the controller
    def getTopo(self):
            get_topo = "/restconf/operational/network-topology:network-topology/topology/flow:1"
            URI = self.ctrl_path + get_topo
            print (URI)
            response = requests.get(URI, auth=(self.username, self.password))
            string_xml =  response.json()
            nodes = []
            links = []
            link_labels = []
            for i in range(len(string_xml['topology'][0]['node'])):
                nodes.append(string_xml['topology'][0]['node'][i]['node-id'])
            for i in range(len(string_xml['topology'][0]['link'])):
                links.append(string_xml['topology'][0]['link'][i]['source']['source-node']+'/'+string_xml['topology'][0]['link'][i]['destination']['dest-node'])
                link_labels.append(string_xml['topology'][0]['link'][i]['source']['source-tp']+'/'+string_xml['topology'][0]['link'][i]['destination']['dest-tp'])
            return nodes,links, link_labels

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
                packet_count = flows[i]["opendaylight-flow-statistics:flow-statistics"]["packet-count"]
                try:
                    instructions_temp = flows[i]['instructions']
                    action = instructions_temp['instruction'][0]['apply-actions']['action'][0]['output-action']['output-node-connector']
                    # print ("Output Port",action)
                except:
                    print ("No instructions!")
                    action = "drop"
                flow_entry = [cookie, priority, match, idle_timeout, hard_timeout, action, packet_count]
                flow_entries.append(flow_entry)
            return flow_entries
            
    # Add a flow to a switch
    def addFlow(self, switch_id, priority, cookie, dest_ip, dest_mask, action):
        add_flow = "/restconf/operations/sal-flow:add-flow"
        URI = self.ctrl_path + add_flow
        headers = {'Content-Type': 'application/xml'} 
        print ("Action: ", action)
        if (action==""):
            payload = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <input xmlns="urn:opendaylight:flow:service">
        <node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="{switch_id}"]</node>
        <table_id>0</table_id>
        <priority>{priority}</priority>
        <cookie>{cookie}</cookie>
        <match>
            <ethernet-match>
                <ethernet-type>
                    <type>2048</type>
                </ethernet-type>
            </ethernet-match>
            <ipv4-destination>{dest_ip}/{dest_mask}</ipv4-destination>
        </match>
        <instructions>
            <instruction>
                <order>0</order>
                <apply-actions>
                    <action>
                        <order>0</order>
                    </action>
                </apply-actions>
            </instruction>
        </instructions>
    </input>'''
        else:
            payload = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
    <input xmlns="urn:opendaylight:flow:service">
        <node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="{switch_id}"]</node>
        <table_id>0</table_id>
        <priority>{priority}</priority>
        <cookie>{cookie}</cookie>
        <match>
            <ethernet-match>
                <ethernet-type>
                    <type>2048</type>
                </ethernet-type>
            </ethernet-match>
            <ipv4-destination>{dest_ip}/{dest_mask}</ipv4-destination>
        </match>
        <instructions>
            <instruction>
                <order>0</order>
                <apply-actions>
                    <action>
                        <output-action>
                            <output-node-connector>{action}</output-node-connector>
                        </output-action>
                        <order>0</order>
                    </action>
                </apply-actions>
            </instruction>
        </instructions>
    </input>'''

        # print (payload)
        r = requests.post(URI, data=payload, headers=headers, auth=(self.username, self.password))
        return r

    # Delete a flow from a switch
    def removeFlow(self, switch_id, priority, cookie, dest_ip, dest_mask):
        delete_flow = "/restconf/operations/sal-flow:remove-flow"
        URI = self.ctrl_path + delete_flow
        headers = {'Content-Type': 'application/xml'} 
        payload = f'''<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<input xmlns="urn:opendaylight:flow:service">
    <node xmlns:inv="urn:opendaylight:inventory">/inv:nodes/inv:node[inv:id="{switch_id}"]</node>
    <table_id>0</table_id>
    <cookie>{cookie}</cookie>
    <priority>{priority}</priority>
    <match>
        <ethernet-match>
            <ethernet-type>
                <type>2048</type>
            </ethernet-type>
        </ethernet-match>
        <ipv4-destination>{dest_ip}/{dest_mask}</ipv4-destination>
    </match>
</input>'''
        # print (payload)
        r = requests.post(URI, data=payload, headers=headers, auth=(self.username, self.password))
        return r


