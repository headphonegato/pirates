import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
import game.display as display

class Samurais(event.Event):
    def __init__ (self):
        self.name = "The Samurais Attack"
    
    def process (self, world):
        result = {}
        result["message"] = "The Samurais have been defeated"
        
    display.announce ("You are attacked by a group of Samurais")
 
    
      
