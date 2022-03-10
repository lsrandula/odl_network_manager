import networkx as nx
import matplotlib.pyplot as plt
import math

# Add nodes and edges

def remove_leading(str_var):
    while str_var[0] == "0" or str_var[0]==":":
            str_var = str_var[1:]
    return (str_var)

def topology_img(Links, link_labels):
    plt.clf()
    G=nx.Graph()
    edge_labels = {}
    # print (len(Links))
    for i in range(len(Links)):
        # print (Links[i])
        nodes = Links[i].split("/")
        for j in range(len(link_labels[i])):
            temp = link_labels[i].split("/")
            for k in range(len(temp)):
                if "host" in temp[k]:
                    temp[k] = "h" + remove_leading(temp[k][4:])
                elif "openflow" in temp[k]:
                    temp[k] = "s" + temp[k][8:]
            link_labels[i] = temp[0]+"/"+temp[1]
        G.add_edge(nodes[0], nodes[1], labels=link_labels[i])
        print ()
        

    # pos=nx.shell_layout(G)
    pos=nx.spring_layout(G, scale=3, k=1.8/math.sqrt(G.order()))
    nx.draw(G, pos, with_labels = True, font_size=5)
    nx.draw_networkx_edge_labels(G, pos, font_size=4, font_color= "red", clip_on=True )
    x_values, y_values = zip(*pos.values())
    x_max = max(x_values)
    x_min = min(x_values)
    x_margin = (x_max - x_min) * 0.25
    plt.xlim(x_min - x_margin, x_max + x_margin)
    plt.savefig('static/images/topology.png', dpi=200)
    print ("Output Topology Image")