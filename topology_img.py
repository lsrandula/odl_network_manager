import networkx as nx
import matplotlib.pyplot as plt

# Links = ['host:00:00:00:00:00:01/openflow:1:1', 'openflow:1:2/host:00:00:00:00:00:02', 'openflow:1:1/host:00:00:00:00:00:01', 'host:00:00:00:00:00:02/openflow:1:2']

# Add nodes and edges

def topology_img(Links, link_labels):
    plt.clf()
    G=nx.Graph()
    edge_labels = {}
    # print (len(Links))
    for i in range(len(Links)):
        # print (Links[i])
        nodes = Links[i].split("/")
        # if len(nodes)<2:
        #     nodes.append(nodes[0])
        # for j in range(2):
        #     if "openflow" in nodes[i]:
        #         switch_temp = nodes[i].split(":")
        #         nodes[i] = switch_temp[0]+":"+switch_temp[1]
        # print (type(node[0]))
        # edge_labels[node[0],node[1]] = link_labels[i]
        G.add_edge(nodes[0], nodes[1], labels=link_labels[i])
        print ()
        

    # pos=nx.shell_layout(G)
    pos=nx.spring_layout(G, scale=3)
    nx.draw(G, pos, with_labels = True, font_size=8)
    # nx.draw_networkx_edge_labels(G, pos)
    nx.draw_networkx_edge_labels(G, pos, font_size=4, font_color= "red", clip_on=True )
    x_values, y_values = zip(*pos.values())
    x_max = max(x_values)
    x_min = min(x_values)
    x_margin = (x_max - x_min) * 0.25
    plt.xlim(x_min - x_margin, x_max + x_margin)
    # larger figure size
    # plt.figure()
    plt.savefig('static/images/topology.png', dpi=200)
    print ("Output Topology Image")