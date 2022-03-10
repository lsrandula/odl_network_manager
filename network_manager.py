import controller_comm
import topology_img

odl0 = controller_comm.ODL_Controller()

def view_topology():
        print ("...View Topology...")
        topology = odl0.getTopo()
        print ("Nodes: ",topology[0],"\nLinks: ",topology[1])
        topology_img.topology_img(topology[1],topology[2])
        

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
        datapath_id = "openflow:"+switch_num
        flow_entries = odl0.getFlowStat(datapath_id)
        for i in range(len(flow_entries)):
                print ("cookie: ", flow_entries[i][0], ", priority:", flow_entries[i][1], ", match: ", flow_entries[i][2], ", idle-timeout: ", flow_entries[i][3], ", hard-timeout: ", flow_entries[i][4], ", outport-port/action: ", flow_entries[i][5], ", packet count: ", flow_entries[i][6])
        return flow_entries

def add_flow(switch_id, priority, cookie, dest_ip, dest_mask, action):
        print ("...Add a Flow...")
        return odl0.addFlow(switch_id, priority, cookie, dest_ip, dest_mask, action)


def remove_flow(switch_id, priority, cookie, dest_ip, dest_mask):
        print ("...Remove a Flow...")
        return odl0.removeFlow(switch_id, priority, cookie, dest_ip, dest_mask)