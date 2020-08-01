"""
Helps to visualize the relationship
"""
import os
import time
import networkx as nx
import matplotlib.pyplot as plt
from tracker.tracker import utils


def create_visualization(tracker):
    """
    Creates a visualization for direct contacts for the given peron
    :param tracker: Tracker details of the Person
    :return: Image
    """
    graph = nx.DiGraph()
    graph.add_node(tracker.person_id)

    for person in tracker.get_persons_related:
        graph.add_node(person.social_no)
        graph.add_edge(tracker.person_id, person.social_no)

    pos = nx.spring_layout(graph)
    nx.draw(graph, pos, with_labels=True, arrows=False)

    time_str = time.strftime("%Y%m%d-%H%M%S")
    image_name = '{}_track_{}.png'.format(tracker.person_id, time_str)
    output_dir = os.environ['TRACKER_GRAPH_FOLDER']
    path = output_dir + r'\\' + image_name
    utils.delete_file_if_exists(path)
    plt.savefig(path)
    temp_out = os.environ['TRACKER_HTTP_SERVER'] + r'/' + image_name
    return temp_out
