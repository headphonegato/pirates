from game.display import menu
import game.combat as combat
import game.context as context
import game.superclasses as superclasses
import random

class Item(superclasses.ActionResolver, context.Context):
    def __init__(self, name, value):
        superclasses.ActionResolver.__init__(self)
        context.Context.__init__(self)
        self.name = name
        self.value = value
        self.damage = (0,0)
        self.firearm = False
        self.charges = 0
        self.usedUp = False
        self.skill = None
        self.verb = None
        self.verb2 = None

    def __str__(self):
        return f"{self.name} ({self.getValue()} shillings)"

    def __lt__(self, other):
        return self.name < other.name

    def getValue(self):
        return self.value

    def ready(self):
        return (self.firearm == False or self.charges > 0)

    def discharge(self):
        if(self.firearm):
            self.charges -= 1

    def recharge(self, owner):
        if self.firearm == True and self.charges == 0 and owner.powder > 0:
            self.charges = 1
            owner.powder -= 1

    def getAttacks(self, owner):
        attacks = []
        if self.damage[1] > 0 and not self.verb is None and not self.verb2 is None and self.skill in owner.skills.keys() and self.ready():
            attacks.append(superclasses.CombatAction(f"{self.verb} with {self.name}", superclasses.Attack(self.name, self.verb2, owner.skills[self.skill], self.damage, self.firearm), self))

        return attacks

    def pickTargets(self, action, attacker, allies, enemies):
        options = []
        for t in enemies:
            options.append(f"attack {t.name}")
        choice = menu (options)
        return [enemies[choice]]

    def resolve(self, action, moving, chosen_targets):
        super().resolve(action, moving, chosen_targets)
        if(isinstance(action.action, superclasses.Attack)):
            if (action.action.gunshot == True):
                self.discharge()


class Cutlass(Item):
    def __init__(self):
        super().__init__("cutlass", 5) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,60)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"

class BelayingPin(Item):
    def __init__(self):
        super().__init__("belaying-pin", 1) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (5,30)
        self.skill = "melee"
        self.verb = "bash"
        self.verb2 = "bashes"

class Flintlock(Item):
    def __init__(self):
        super().__init__("flintlock", 400) #Note: price is in shillings (a silver coin, 20 per pound)
        self.damage = (10,100)
        self.firearm = True
        self.charges = 1
        self.skill = "guns"
        self.verb = "shoot"
        self.verb2 = "shoots"

class Lightning_Attack():
    """Basic attack object, with a name, description, chance of success, and damage range. Sufficient for specifying monster attacks."""
    def __init__ (self, name, description, success, damage_range):
        self.name = name
        self.description = description
        self.success = success
        self.damage_range = damage_range
        self.gunshot = False

    def __eq__(self, other):
        if not isinstance(other):
            return False
        if self.name == other.name and self.description == other.description and self.success == other.success and self.damage_range == other.damage_range:
            return True
        return False

class Lightning_sword(Item):
    def __init__(self):
        super().__init__("lightning_sword", 1) #will change the 1 later 
        self.damage =  (50,70)
        self.skill = "swords"
        self.verb = "slash"
        self.verb2 = "slashes"
        #self.verb = "lightning_bolts"
        #self.verb = "electric_slash"

    def getAttacks(self, owner):
        attacks = []
        if "swords" in owner.skills.keys():
            attacks.append(superclasses.CombatAction(f"{self.verb} with {self.name}", superclasses.Attack(self.name, self.verb2, owner.skills[self.skill], self.damage, False), self))
        #What does a lightning bolt do
        attacks.append(superclasses.CombatAction(f"zap with {self.name}", Lightning_Attack("lightning","blasts",50,(60,70)), self))
        return attacks

    def pickTargets(self, action, attacker, allies, enemies):
        options = []
        for t in enemies:
            options.append(f"attack {t.name}")
        choice = menu (options)
        return [enemies[choice]]

class Flame_sword(Item):
    def __init__(self):
        super().__init__("flame_sword")
        self.damage = (40,50)
        self.skill = "swords"
        self.verb = "slash"
        #self.verb = "flame_slash"
        #self.verb = "fireball"
       
    def getAttacks(self, owner):
        attacks = []
        if "swords" in owner.skills.keys():
            attacks.append(superclasses.CombatAction(f"{self.verb} with {self.name}", superclasses.Attack(self.name, self.verb2, owner.skills[self.skill], self.damage, False), self))
        attacks.append(superclasses.CombatAction(f"Flame {self.name}", Flame_sword("Flame","slash",40,(60,80)), self))
        return attacks

    def pickTargets(self, action, attacker, allies, enemies):
        options = []
        for t in enemies:
            options.append(f"attack {t.name}")
        choice = menu (options)
        return [enemies[choice]]

    

