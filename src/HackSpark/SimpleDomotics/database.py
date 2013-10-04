import json
from pyelasticsearch import ElasticSearch


class SensorDatabase(object):

    def __init__(self, server='http://0.0.0.0:9901'):
        self.server = server
        self.es = ElasticSearch(server)

    def index(self, sensor_id, data):
        return self.es.index('domotic', 'sensor_values', data)
