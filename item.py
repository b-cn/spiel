class Item:
    def __init__(self, name, description, movable=False, hidden=False):
        self.name = name
        self.description = description
        self.movable = movable
        self.hidden = hidden

    def __str__(self):
        return self.name