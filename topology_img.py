import networkx as nx
import matplotlib.pyplot as plt

# Links = ['host:00:00:00:00:00:01/openflow:1:1', 'openflow:1:2/host:00:00:00:00:00:02', 'openflow:1:1/host:00:00:00:00:00:01', 'host:00:00:00:00:00:02/openflow:1:2']
G=nx.Graph()


# Add nodes and edges

def topology_img(Links):
    for i in range(len(Links)):
        # print (Links[i])
        nodes = Links[i].split("/")
        if len(nodes)<2:
            nodes.append(nodes[0])
        for i in range(2):
            if "openflow" in nodes[i]:
                switch_temp = nodes[i].split(":")
                nodes[i] = switch_temp[0]+":"+switch_temp[1]
        G.add_edge(nodes[0], nodes[1])

    pos=nx.shell_layout(G)
    nx.draw(G, pos, with_labels = True)
    x_values, y_values = zip(*pos.values())
    x_max = max(x_values)
    x_min = min(x_values)
    x_margin = (x_max - x_min) * 0.25
    plt.xlim(x_min - x_margin, x_max + x_margin)
    plt.savefig('topology.png')
    print ("Output Topology Image")