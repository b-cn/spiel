from item import Item
from player import Player

class ItemContainer(Item):
    def __init__(self,name, description, movable, puzzle=True):
        super().__init__(name, description, movable)
        self.contains = None
        self.puzzle = puzzle

    def show_content(self, player: Player):
        if self.contains:
            player.take_item(self.contains)
            self.contains = None