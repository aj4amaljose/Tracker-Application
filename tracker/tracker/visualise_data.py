"""
Helps to visualize the relationship
"""
import os
import io
import time
import boto3
import networkx as nx
import matplotlib.pyplot as plt
import base64


def visualization_creation_and_s3_push(tracker, aws_push=True):
    """
    Creates a visualization for direct contacts for the given peron

    :param tracker: Tracker details of the Person
    :param aws_push: S3 push required or not
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
    image_data = io.BytesIO()
    plt.savefig(image_data, format='png')
    image_data.seek(0)
    if aws_push and 'TRACKER_AWS_S3_BUCKET' in os.environ:
        aws_bucket = os.environ['TRACKER_AWS_S3_BUCKET']
        s3_client = boto3.client('s3')
        s3_client.put_object(Body=image_data, ContentType='image/png',
                             Bucket=aws_bucket, Key=image_name)
    image_data.seek(0)
    return image_data


def convert_visualization_data(image_data):
    """
    Convert image value for depicting image in html

    :param image_data: image binary data
    """
    image_png = base64.b64encode(image_data.getvalue()).decode('ascii')
    return image_png

