import random
import game.event as event
from game import event
import game.combat as combat
import game.display as display


class SamuraiBoss(event.Event):
    def __init__(self):
        self.name = "The Samurai Boss Appears"

    def process(self, world):
        result = {}
        result["message"] = "The Samurai Boss has been defeated !"
        boss = combat.Samurai("Samurai Boss")
        boss.speed *= 1.5  
        boss.health *= 3.0  
        boss.attack_power *= 2.0  
        boss.special_attack = "Sword Strike"
       
        display.announce("You are challenged by the mighty Samurai Boss!")
        combat.Combat([boss]).combat()
        
        result["newevents"] = [self]
        return result
