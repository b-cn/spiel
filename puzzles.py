import random
from room import Room

class Puzzles:

    def guessing_puzzle(room):
        print("the door is locked. you read the inscription on the door: 'guess the correct number between 1 and 10'")
        correct_number = random.randint(1, 10)
        attempts = 4
        while attempts > 0:
            try:
                guess = int(input("guess the number: "))
                if guess == correct_number:
                    room.locked = False
                    print("the door opens!")
                    return True
                elif guess > correct_number:
                    print("guess too high!")
                else:
                    print("guess too low!")
            except ValueError:
                print("invalid number!")
            attempts -= 1
            print("remaining attempts: ", attempts)
        print("you have failed! the floor starts to collapse under your feet...")
        exit()


