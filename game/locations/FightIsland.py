from game import location
import game.config as config
import game.display as display
import game.event as event
from game.events import samurais
import random
from game.events import samurai_boss


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
        self.event_chance = 0
        self.events.append(samurais.Samurais())

    
    def process_verb (self, verb, cmd_list, nouns):
        if (verb == "south"):
            display.announce ("You made a mistake and you fight the Samurais again.")
            config.the_player.next_loc = self.main_location.locations["Treasure Chest"]
        elif (verb == "north"):
            config.the_player.next_loc = self.main_location.locations["Boss"]
        elif (verb == "east"):
            display.announce ("You went around please go north or go west.")
        elif(verb == "west"):
            config.the_player.next_loc = self.main_location.locations ["key"]
            display.announce ("You see a key in order to get it you must be able to do the puzzle")

class Boss_Fight (location.SubLocation):
    def __init__ (self,m):
        super().__init__(m)
        self.name = "Boss"
        self.symbol = 'B'
        self.visitable = True
        self.locations = {}
        
    
    def trigger_boss_fight (self, ship):
        display.announce ("You have reached the boss of the Samurais fight him")
        boss_event = samurai_boss()
        result = boss_event.process(ship.world)

        if result["message"] == "The Samurai Boss has been defeated!":
            display.announce("You have defeated the Samurai Boss")
        else:
            display.announce("The Samurai Boss remains undefeated. Gather your strength and try again!")
        

class puzzle_with_key (location.SubLocations):
    def __init__ (self,m):
        self.name = "key"
        self.symbol = "K"
        self.visitable = True 
        self.Locations = {}
    
    def trigger_puzzle(self, player, treasure_chest):
        display.announce("You have encountered a puzzle! Solve it to earn the key.")
        if self.play_game():
            player.add_to_inventory(["Key"])
            display.announce("You now have the key!")
            treasure_chest.set_key_item("Key")
        else:
            display.announce("You failed to earn the key. Better luck next time!")

    def play_game(self):
        tries = 0
        wins = 0
        
        while tries < 4:
            display.announce("Choose Rock, Paper, or Scissors: ")
            player_choice = input("Your choice: ").capitalize()

            if player_choice not in ["Rock", "Paper", "Scissors"]:
                display.announce("Invalid choice! Please choose Rock, Paper, or Scissors.")
                continue
            result, won = self.rock_paper_scissors(player_choice)
            display.announce(result)
            if won:
                wins += 1
            tries += 1
            if wins > 0:
                display.announce("Congratulations! You have won the puzzle and earned the key!")
                return True
        display.announce("Sorry you did not win the puzzle. Try again next time!")
        return False

    def rock_paper_scisiors (self,player_choice): 
        choices = ["Rock", "Paper", "Scicsors"]
        Ai_guessing = random.choice(choices)

        if player_choice == Ai_guessing:
            return "It's a tie!", False
        elif (player_choice == "Rock" and Ai_guessing == "Scissors") or \
             (player_choice == "Paper" and Ai_guessing == "Rock") or \
             (player_choice == "Scissors" and Ai_guessing == "Paper"):
            return f"You win! {player_choice} beats {Ai_guessing}.", True
        else:
            return f"You lose! {Ai_guessing} beats {player_choice}.", False 


class Flame_sword(Item):
    def __init__(self):
        super().__init__("flame_sword")
        self.damage = (40,50)
        self.skill = "swords"
        self.verb = "slash"

               

class TreasureChest(location.SubLocation):
    def __init__(self, m):
        super().__init__(m)
        self.name = "Treasure Chest"
        self.symbol = "F"
        self.visitable = True
        self.contains_item = False
        self.key_required = False
        self.key_item = None

    def set_key_item(self, key):
        self.key_item = key
        self.key_required = True
    
    def open_chest(self, player):
         if self.key_required:
            if self.key_item in player.inventory:
                flame_sword = Flame_sword()
                player.add_to_inventory([flame_sword])
                self.contains_item = True 
                display.announce("You have opened the chest and obtained the Flame Sword!")
                return True
            else:
                display.announce("You don't have the key to open this chest.")
                return False
         else:
            display.announce("This chest doesn't require a key to open.")
            return False
    
    