"""
Helps to visualize the relationship
"""
import os
import networkx as nx
import matplotlib.pyplot as plt


def create_visualization(tracker):
    """
    Creates a visualization for direct Nodes
    :param tracker: Tracker details of the Person
    :return: Image
    """
    graph = nx.DiGraph()
    graph.add_node(tracker.person_id)
    for person in tracker.get_persons_related:
        graph.add_node(person.social_no)
        graph.add_edge(tracker.person_id, person.social_no)
    plt.title('{}_track'.format(tracker.person_id))
    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, arrows=False)
    image_name = '{}_track.png'.format(tracker.person_id)
    ouput_dir = os.environ['TRACKER_GRAPH_FOLDER']
    path = ouput_dir + r'\\' + image_name
    plt.savefig(path)
    temp_out = os.environ['TRACKER_HTTP_SERVER'] + r'/' + image_name
    return temp_out
