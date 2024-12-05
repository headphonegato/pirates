from game import location
import game.config as config
import game.display as display
import game.event as event
from game.events import samurais


class Fight_Island (location.Location):

    def __init__ (self, x, y, w):
        super().__init__(x, y, w)
        self.name = "FightIsland"
        self.symbol = 'FI'
        self.visitable = True
        self.locations = {}
        self.starting_location = self.locations["Shrine Temple"]

    def enter (self, ship):
        display.announce ("You have arrived at the Fighting Island get ready to fight with your life")
    
class Temple (location.SubLocation):
    def __init__ (self, m):
        super().__init__(m)
        self.name = "Shrine Temple"
        self.verbs['north'] = self
        self.verbs['south'] = self 
        self.verbs['east'] = self
        self.verbs['west'] = self
        self.events.append(samurais.Samurais())

    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You made a mistake and you fight the Samurais again.")
            self.main_location.end_visit()
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Big Samurai"]
        elif (verb == "east" or verb == "west"):
            display.announce ("You went around please go north.")

    def __init__ (self,m):
        super().__init__(m)
        self.name = "Boss"
        self.symbol = 'B'
        self.visitable = True
        self.locations = {}
    
    def enter (self, ship):
        display.announce ("You have reached the boss of the Samurais fight him for a reward")


    
    