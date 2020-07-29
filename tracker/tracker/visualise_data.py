"""
Helps to visualize the relationship
"""
import networkx as nx
from networkx.drawing.nx_agraph import graphviz_layout
import matplotlib.pyplot as plt


def create_visualization(tracker):
    """
    Creates a visualization for direct Nodes
    :param tracker: Tracker details of the Person
    :return: Image
    """
    G = nx.DiGraph()
    G.add_node(tracker.person_id)
    for person in tracker.get_persons_related:
        G.add_node(person.social_no)
        G.add_edge(tracker.person_id, person.social_no)
    nx.nx_agraph.write_dot(G, 'test.dot')
    plt.title('draw_networkx')
    pos = graphviz_layout(G, prog='dot')
    nx.draw(G, pos, with_labels=False, arrows=False)
    plt.savefig('nx_test.png')