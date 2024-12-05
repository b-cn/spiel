import player
from item import Item
from item_container import ItemContainer
from player import Player
from room import Room
from puzzles import Puzzles
import json

class Game:
    def __init__(self):
        self.entrance = Room("entrance", "its the entrance")
        self.chamber = Room("chamber", "its the chamber")
        self.crawl = Room("crawl space", "narrow place, not high enough to stand in")
        self.hall = Room("hall of doom", "its the hall of doom", locked=True)
        self.treasure = Room("treasure room", "you've made it. the air feels heavy with the scent of gold and silver", locked=True)
        self.sanctuary = Room("sanctuary", "its the sanctuary")
        self.player = Player(self.entrance)

        self.entrance.add_connected_room("north", self.chamber)
        self.chamber.add_connected_room("west", self.crawl)
        self.crawl.add_connected_room("east", self.chamber)
        self.chamber.add_connected_room("south", self.entrance)
        self.chamber.add_connected_room("east", self.hall)
        self.hall.add_connected_room("west", self.chamber)
        self.hall.add_connected_room("north", self.treasure)
        self.treasure.add_connected_room("south", self.hall)

        self.ladder = Item("ladder", "its an old wooden ladder, useful for reaching heights", movable=True)
        self.hole = ItemContainer("hole", "its a hole in the wall up above, you're too short to reach it", movable=False)
        self.key = Item("key", "its a wooden key shaped like a toothbrush", hidden=True)
        self.jars = ItemContainer("jars", "its jars", movable=False)
        self.statue = Item("statue", "its a statue", movable=False)
        self.blub=Item("oblub", "its an oblub", movable=False)

        self.hole.contains = self.key

        self.entrance.add_item(self.ladder)
        self.entrance.add_item(self.blub)
        self.chamber.add_item(self.hole)
        self.crawl.add_item(self.jars)
        self.chamber.add_item(self.statue)


    def ladder_puzzle(self):
        if self.ladder in self.player.inventory:
            self.hole.puzzle = False
            print("you use the ladder to reach the hole")
        else:
            print("you try and fail to reach the hole")

    def key_puzzle(self):
        if self.key in self.player.inventory:
            self.hall.locked = False
            print("you use the key to unlock the door")
            return True
        else:
            return False

    def check_move(self, direction):
        next_room = self.player.current_room.connected_rooms[direction]
        if next_room.locked:
            print(f"The room to the {direction} is locked.")
            return False
        self.player.move(direction)
        print(f"You moved to the {self.player.current_room.name}.")
        return True

    def unlock_room(self, room, direction):
        if room.name == "hall of doom" and self.key_puzzle():
            return self.check_move(direction)
        elif room.name == "treasure room" and Puzzles.guessing_puzzle(room):
            return self.check_move(direction)
        print(f"The room to the {direction} remains locked.")
        return False

    def move_rooms(self):
        print("Move where?")
        directions = self.player.current_room.connected_rooms.keys()
        for dir in directions:
            print(f"{dir}")
        move_choice = input("Choose a direction: ")
        if move_choice in directions:
            if not self.check_move(move_choice):
                next_room = self.player.current_room.connected_rooms[move_choice]
                if not self.unlock_room(next_room, move_choice):
                    print("fds")
        else:
            print("Invalid direction.")

    def inspect_item(self,item):
        print(item.description)

        if item == self.hole and self.player.current_room == self.chamber:
            self.ladder_puzzle()

        if isinstance(item, ItemContainer) and not item.puzzle:
            print(f"you take a closer look at the {item.name}.")
            if item.contains:
                print("there is a", item.contains.name,"!")
                print("you have picked up the", item.contains.name)
                item.show_content(self.player)
            else:
                print("there is nothing here")

        elif item.movable:
            take_choice = input(f"pick up the {item.name}? y/n: ")
            if take_choice.lower() == "y":
                self.player.take_item(item)
        else:
            print(f"it's just a {item.name}")

    def look(self):
        # if self.player.current_room.name == "treasure room":
        #     self.treasure_ev()
        print(self.player.current_room.describe())
        items = self.player.current_room.items
        if items:
            print("what do you want to inspect? enter the name")
            choice = input("> ")
            matching_item = False
            for i in items:
                if choice.lower() == i.name:
                    matching_item = True
                    self.inspect_item(i)
            if not matching_item:
                print(f"there is nothing called '{choice}' to inspect here")
        else:
            print("the room is empty")

    def game_loop(self):
        print("you have decided to rob a pyramid. good luck")
        while True:
            if self.player.inventory:
                print("-- you currently have:")
                for i in self.player.inventory:
                    print("---",i)
            print("what do you want to do? enter the corresponding number")
            print("1 look around")
            print("2 move")
            print("3 save")
            print("4 quit")
            print("5 load game")
            choice = input("your choice: ")
            if choice == "1":
                self.look()
            elif choice == "2":
                self.move_rooms()
            elif choice == "3":
                self.save()
            elif choice == "4":
                print("you have decided to turn back and live an honest life")
                break
            elif choice == "5":
                self.load()
            else:
                print("invalid choice. choose 1, 2, or 3")

    def start(self):
        print("starting game")
        self.game_loop()
        print("game over")

    def save(self):
        try:
            data = {
                "player": {
                    "current_room": self.player.current_room.name,
                    "inventory": [{"name": item.name} for item in self.player.inventory],
                },
                "rooms": {
                    room.name: {
                        "locked": room.locked,
                        "items": [
                            {
                                "name": item.name,
                                "type": "ItemContainer" if isinstance(item, ItemContainer) else "Item",
                                "contains": item.contains.name if isinstance(item,
                                                                             ItemContainer) and item.contains else None,
                                "puzzle": item.puzzle if isinstance(item, ItemContainer) else None,
                            }
                            for item in room.items
                        ],
                    }
                    for room in [self.entrance, self.chamber, self.crawl, self.hall, self.treasure, self.sanctuary]
                },
            }
            with open("savefile.json", "w") as f:
                json.dump(data, f, indent=4)
            print("Game saved successfully.")
        except Exception as e:
            print(f"An error occurred while saving the game: {e}")

    def load(self):
        try:
            with open("savefile.json", "r") as f:
                data = json.load(f)

            rooms = {
                room.name: room
                for room in [self.entrance, self.chamber, self.crawl, self.hall, self.treasure, self.sanctuary]
            }
            self.player.current_room = rooms[data["player"]["current_room"]]
            self.player.inventory = [
                next(item for item in self.player.inventory if item.name == item_data["name"])
                for item_data in data["player"]["inventory"]
            ]

            for room_name, room_data in data["rooms"].items():
                room = rooms.get(room_name)
                if room:
                    room.locked = room_data["locked"]
                    room.items = []
                    for item_data in room_data["items"]:
                        if item_data["type"] == "ItemContainer":
                            item = ItemContainer(
                                item_data["name"],
                                "description placeholder",  # Descriptions can be hardcoded if they don't change
                                movable=False,  # Default values, adjust based on logic
                                puzzle=item_data["puzzle"],
                            )
                            if item_data["contains"]:
                                item.contains = next(
                                    obj for obj in self.player.inventory if obj.name == item_data["contains"]
                                )
                        else:
                            item = Item(
                                item_data["name"],
                                "description placeholder",  # Descriptions can be hardcoded
                                movable=True,  # Adjust based on default logic
                            )
                        room.items.append(item)

            print("Game loaded successfully.")
        except FileNotFoundError:
            print("No save file found.")
        except Exception as e:
            print(f"An error occurred while loading the game: {e}")


    # def treasure_ev(self):
    #         choice = input("take the stuff? y/n: ")
    #         if choice.lower() == "y":
    #             print("you grab handfuls of golden jewelry and shove it into your bag")
    #             if - bedingung -
    #                 print("suddenly, you hear a noise")
    #                 self.treasure.add_connected_room("east", self.sanctuary)
    #                 self.player.move("east")
    #                 print("the wall in front of you appears to have moved, leaving an opening just big enough to fit through")
    #                 print("you step forward and find yourself in an empty room...")
    #                 print("...empty, save for the sarcophagus at its centre")
    #                 print("thud! you look back. the crack in the wall has disappeared")
    #                 print("you're trapped")
    #                 print("you stare at the painted face on the tomb. it stares back")
    #                 exit()
    #             else:
    #                 print("the end")
    #         if choice.lower() == "n":
    #             print("you go back home")






