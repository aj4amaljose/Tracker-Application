"""
Helps to visualize the relationship
"""
import os
import networkx as nx
import matplotlib.pyplot as plt


def create_visualization(tracker, local=True):
    """
    Creates a visualization for direct contacts for the given peron
    :param tracker: Tracker details of the Person
    :param local:
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
    if local:
        temp_out = os.environ['TRACKER_HTTP_SERVER'] + r'/' + image_name
        """Temporary hack for showing local images in browser, as browser security won't allow. 
        Read through https://chrome.google.com/webstore/detail/web-server-for-chrome/ofhbbkphhbklhfoeikjpcbhemlocgigb """
    else:
        temp_out = None
        # todo Write code to push file to another location and get the URL for the graph image
    return temp_out
