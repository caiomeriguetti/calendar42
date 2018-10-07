from app.resources import PathResource

main_routes = [
    ('/best-path/{points}', PathResource())
]