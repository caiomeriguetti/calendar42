class Graph(object):
    connections = None
    costs = None

    def __init__(self, connections=None, costs=None):
        self.connections = connections
        self.costs = costs

    def set_connections(self, connections):
        self.connections = connections

    def set_costs(self, costs):
        self.costs = costs

    def contains(self, p):

        id = self.get_id(p)

        return id in self.connections

    def get_id(self, p):
        return '%s:%s' % (p['lat'], p['lng'])

    def equals(self, p1, p2):
        return p1['lat'] == p2['lat'] and p1['lng'] == p2['lng']
