from resources import PathResource


def add_routes(api):
    api.add_route('/best-path/{p1}/{p2}', PathResource())