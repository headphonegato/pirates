from game import location
import game.config as config
import game.display as display
from game.events import *
import game.items as items
import game.combat as combat
import game.event as event
from game import event
from game.combat import Monster
import game.items as items
import random
from game.events import seagull
from game.items import Lightning_sword


class Js (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Js"
        self.symbol = 'JS'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["color_guess"] = Color_guess(self)

        self.starting_location = self.locations["beach"]
    
class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self 
        self.verbs['east'] = self
        self.verbs['west'] = self
    
    def enter (self, ship):
        display.announce ("arrived at an island that is very strange and you look at the sky and see random gocolors for some reason", pause=False)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship and look like a fool .")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["color_guess"]
        elif (verb == "east" or verb == "west"):
            display.announce (f"You walk all the way around the island on the beach. and find a powerfull weapon {Lightning_sword} ")

class Color_guess(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "color_guess"
        self.event_chance = 10
        self.events.append(seagull.Seagull())
    
    def guess_color(self):
        colors = ["red", "blue", "green", "black", "Yellow", "orange", "purple",]
        color = random.choice(colors)
        atempts = 0 
        max_attempts = 6 
        guessed_number = False 
        while not guessed_number and atempts < max_attempts:
            guess = input("Guess the color You have 6 attemots: ").lower()
            atempts +=1
            if guess == color:
                guessed_number = True 
                print(f"you have guessd the color correctly {color}")
            else:
                print("Incorrect. Please guess agian")
        if not guessed_number:
            print(f"you've reached the maximum attempts. The color was '{color}'. Goodbye :)")
