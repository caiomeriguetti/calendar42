from app.resources import PathResource


def add_routes(api):
    api.add_route('/best-path/{points}', PathResource())