class Router:
    def __init__(self):
        self.routes = {}
    
    def register(self, route, screen_class):
        self.routes[route] = screen_class

    def resolve(self, route):
        return self.routes.get(route, None)
    
    