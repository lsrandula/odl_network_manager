import controller_comm

odl0 = controller_comm.ODL_Controller()

# print ("Select a function : \n1)View topology\n2)View flow entries\n3)Add a flow\n4)Delete a flow")

# select = int(input("Selection : "))

def view_topology():
        print ("...View Topology...")
        topology = odl0.getTopo()
        print ("Nodes: ",topology[0],"\nLinks: ",topology[1])

def get_switchlist():
        # print a list of OF switches
        print ("List of Switches")
        topology = odl0.getTopo()
        switches = []
        for i in range(len(topology[0])):
                if (topology[0][i][:9]=="openflow:"):
                        switches.append(topology[0][i])
        print ("Switches: ", switches)
        return switches

def view_flowentries(switch_num):
        print ("...View Flow Entries...")
        # # print a list of OF switches
        # topology = odl0.getTopo()
        # switches = []
        # for i in range(len(topology[0])):
        #         if (topology[0][i][:9]=="openflow:"):
        #                 switches.append(topology[0][i])
        # print ("Switches: ", switches)
        # switch_num = input("Select an OF switch: ")
        datapath_id = "openflow:"+switch_num
        # each in flow_entry = [cookie, priority, match, idle_timeout, hard_timeout] format
        flow_entries = odl0.getFlowStat(datapath_id)
        for i in range(len(flow_entries)):
                print ("cookie: ", flow_entries[i][0], ", priority:", flow_entries[i][1], ", match: ", flow_entries[i][2], ", idle-timeout: ", flow_entries[i][3], ", hard-timeout: ", flow_entries[i][4])
        return flow_entries

def add_flow():
        print ("...Add a Flow...")
        # print a list of OF switches
        datapath_id = input("Select an OF switch:")
        # print (odl0.addFlow(datapath_id, flow_id))


def delete_flow():
        print ("...Delete a Flow...")
        # print a list of OF switches
        datapath_id = input("Select an OF switch:")
        # print (odl0.deleteFlow(datapath_id, flow_id))


