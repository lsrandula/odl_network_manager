import controller_comm

S
odl0 = controller_comm.ODL_Controller()
print ("Select a function : \n1)View topology\n2)View flow entries\n3)Add a flow\n4)Delete a flow")

select = int(input("Selection : "))

if (select==1):
        print ("...View Topology...")
        # print (odl0.getTopo())


elif (select==2):
        print ("...View Flow Entries...")
        # print a list of OF switches
        datapath_id = input("Select an OF switch:")
        # print (odl0.getFlowStat())

elif (select==3):
        print ("...Add a Flow...")
        # print a list of OF switches
        datapath_id = input("Select an OF switch:")
        # print (odl0.addFlow(datapath_id, flow_id))


elif (select==4):
        print ("...Delete a Flow...")
        # print a list of OF switches
        datapath_id = input("Select an OF switch:")
        # print (odl0.deleteFlow(datapath_id, flow_id))


