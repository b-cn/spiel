import item

class Room:
    def __init__(self, name, description, locked=False):
        self.name = name
        self.description = description
        self.items = []
        self.connected_rooms ={}
        self.locked=locked

    def add_item(self, item):
        self.items.append(item)

    def add_connected_room(self, direction, room):
        self.connected_rooms[direction] = room

    vovels = ['a', 'e', 'i', 'o', 'u']

    def describe(self):
        description = []
        description.append(self.name)
        description.append(self.description)
        if self.items:
            for i in self.items:
                if i.name[0] in self.vovels:
                    description.append(f"you see an {i.name}")
                elif i.name[-1] == "s":
                    description.append(f"you see {i.name}")
                else:
                    description.append(f"you see a {i.name}")
        return "\n".join(description)

