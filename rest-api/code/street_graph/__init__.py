class Graph(object):
    connections = None
    costs = None

    def __init__(self, connections, costs):
        self.connections = connections
        self.costs = costs

    def contains(self, p):
        return p.id in self.connections


class Point(object):
    def __init__(self, coords):
        self.connections = {}
        self.coords = coords
        self.id = ':'.join([str(coords['lat']), str(coords['lng'])])

    def connect(self, p):
        p.connections[self.id] = self
        self.connections[p.id] = p

    def equals(self, p):
        return p.coords['lat'] == self.coords['lat'] and p.coords['lng'] == self.coords['lng']