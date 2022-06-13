from Area import Point

class BeachBar(Point):
    def __init__(self, name,  lat, lon):
        super().__init__(lat, lon)
        self.name = name



