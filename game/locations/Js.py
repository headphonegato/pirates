from game import location
import game.config as config
import game.display as display
from game.events import *
import game.combat as combat
import game.event as event
from game import event
from game.combat import Monster
import game.items as items
import game.items as item
import random
from game.events import seagull

class Js (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "Js"
        self.symbol = 'J'
        self.visitable = True
        self.locations = {}
        self.locations["beach"] = Beach_with_ship(self)
        self.locations["color_guess"] = Color_guess(self)

        self.starting_location = self.locations["beach"]
   
    def enter (self, ship):
        display.announce ("arrived at my island")
    
class Beach_with_ship (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "beach"
        self.verbs['north'] = self
        self.verbs['south'] = self 
        self.verbs['east'] = self
        self.verbs['west'] = self
    
    def enter (self):
        display.announce ("arrived at an island that is very strange and you look at the sky and see random colors for some reason", pause=False)

    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You return to your ship and guess why have you came back?.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["color_guess"]
        elif (verb == "east" ):
            display.announce (f"You walk all the way around the island on the beach. and find a treasure chest")
        elif (verb == "west"):
            config.the_player.next_loc = self.main_location.locations["treasure"]
            display.announce ("You find a treasure with a item.")

class treasure (location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "treasure"
        self.visitable = True
        self.verbs['north'] = self
        self.verbs['south'] = self
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.verbs['take'] = self
        self.item_in_chest = items.Lightning_sword()
        display.announce("You see the treasure infront of you")
    
    def process_verb (self, verb, cmd_list, nouns):
       if (verb == "south" or verb == "north" or verb == "east" or verb == "west"):
            config.the_player.next_loc = self.main_location.locations["beach"]
       if verb == "take":
        if len(cmd_list) > 1 and (cmd_list[1] == "lightning_sword" or cmd_list[1] == "all"):
            item = self.item_in_chest
            display.announce(f"You open the chest and take the {item.name}.")
            config.the_player.add_to_inventory([item])
            self.item_in_chest = items.lightning_sword()
           
class Lightning_sword(item.Item):
    def __init__(self):
        super().__init__("lightning_sword", 1) #will change the 1 later 
        self.damage =  (50,70)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class Color_guess(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "color_guess"
        self.visitable = True
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
        if guessed_number == max_attempts:
            print(f"you've reached the maximum attempts. The color was '{color}'. Goodbye :)")
