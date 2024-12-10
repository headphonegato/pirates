import game.event as event
import random
import game.combat as combat
import game.superclasses as superclasses
import game.display as display

class Samurais(event.Event):
    def __init__(self):
        self.name = "The Samurais Attack"

    def process(self, world):
        result = {}
        result["message"] = "The Samurais have been defeated!"
        samurais = []
        min_count = 2
        max_count = 4
    
    if random.randrange() < 0.25:  
            max_count = 1
            leader = combat.Samurai("Samurai Leader")
            leader.speed *= 1.3  # Buff speed
            leader.health *= 1.5  # Buff health
            samurais.append(leader)
        
    n_appearing = random.randrange(min_count, max_count)
    for i in range(1, n_appearing + 1):
        samurais.append(combat.Samurai(f"Samurai {i}"))

        display.announce("You are attacked by a group of Samurais!")
        combat.Combat(samurais).combat()
        result["newevents"] = [self]
        return result
    

   
    
      
