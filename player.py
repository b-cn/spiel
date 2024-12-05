
class Player:
    def __init__(self, start):
        self.current_room = start
        self.inventory = []

    def move(self, direction):
        self.current_room = self.current_room.connected_rooms[direction]

    def take_item(self, item):
        self.inventory.append(item)
        if not item.hidden:
            self.current_room.items.remove(item)

    #def show_inventory(self):
