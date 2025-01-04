import random
class Character:
    #This section defines all stats and their max amounts for function calculations
    def __init__(self, name, health, armour, attack_power, armour_attack_power, evade_chance, special_point_amount):
        self.name = name
        self.health = health
        self.armour = armour
        self.attack_power = attack_power
        self.max_health = health  
        self.max_armour = armour
        self.armour_attack_power = armour_attack_power
        self.evade_chance = evade_chance
        self.special_points = special_point_amount
        self.special_points_max = special_point_amount
    
    def attack_armour(self, opponent):
        armour_damage = min(self.armour_attack_power, opponent.armour)
        opponent.take_armour_damage(armour_damage)
        print(f"\n{self.name} attacks {opponent.name} Armour for {self.armour_attack_power} damage!")
       #attack opponent health
    def attack_health(self, opponent):
        # damage calculation with armour mechanic. Overall damage to player health is: (attack power - armour health)
        effective_damage = max(0, self.attack_power - opponent.armour)
        print(f"\n{self.name} attacks {opponent.name} for {effective_damage} damage!")
        # dodge mechanic randomizes value 1/100 and takes from class specific value 
        if random.randint(0,100) <= opponent.evade_chance:
            print(f"\n{opponent.name} dodged the attack!")
            return
        else:
            opponent.take_damage(effective_damage)
        # so each class has a % dodge value
    #method for taking damage so that classes can override damage taking mechanics 
    #with their specific abilities  
    #This function applies armour damage to armour stat
    def take_armour_damage(self, armour_damage):
        self.armour -= armour_damage
    #This function calculates final damage with randomization and applies to entity
    def take_damage(self, damage):
        #final_damage is base damage + or - 2 using randomizer
        final_damage = damage + random.randint(-2,2)
        #final_damage_floor ensure that damage does not go negative if armour negates damage and recieves -2 or -1 from randomizer
        final_damage_floor = max(final_damage, 0)
        #this uses same logic as above to clamp health to zero
        self.health = max(self.health - final_damage_floor, 0)
        print(f"\n{self.name} takes {final_damage_floor} damage! Health left: {self.health}")
    #This function detracts 1 from special attribute. format self.XXX(1) to subtract 1.
    # It is not a clamped value because game logic will not allow player to use a special ability if value <= 0
    def expend_special_point(self, special):
        self.special_points -= special
        print(f"\n{self.name} expends {special} ability point! Ability points left: {self.special_points}")
    #this function displays stats relevant to battle
    def display_stats(self):
        print(f"\n{self.name}'s Stats - Health: {self.health}/{self.max_health}, Armour: {self.armour}/{self.max_armour}, Attack Power: {self.attack_power}, Armour Attack Power: {self.armour_attack_power}, Special Points: {self.special_points}/{self.special_points_max}" )
    # This function heals the player. heal_amount is classified within each character/wizard. 
    # min function clamps to make sure self.max_health is what self.health is set to if heal_amount would go over cap
    def heal(self, heal_amount):
        self.health = min(self.max_health, self.health + heal_amount)
        print(f"\n{self.name} healed for {heal_amount}! Health: {self.health}/{self.max_health}")
            

# Warrior class
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health = 80, armour = 20, attack_power = 12, armour_attack_power = 3, evade_chance= 15, special_point_amount= 2)
        self.block_active = False #block ability off by default
        self.block_odds = 30 #30% chance to block attack if block is active
        self.block_percent = 50 #succesful block reduces incoming damage by 50%
    #class specific heal value but calling to parent function heal
    def heal(self):
        super().heal(20)
    #pull_specials is unique to each class to give descriptions of each ability
    def pull_specials(self):   
        print("1. Raise Shield(Passive): Buff that gives player chance to negate incoming damage.")
        print("2. Restore Armour: Player restores armour back to max level.")
        print("3. Go back.")
    #activate_special one and two activate corresponding ability-- common to each class but consquence of function unique to class
    def activate_special_one(self):
        #activates block condition which modifies take_damage logic
        self.block_active = True 
        self.expend_special_point(1)
        #expends special ability point
    def use_special_ability_2(self):
        #activates warrior specific heal armour ability
        self.heal_armour()
        self.expend_special_point(1)

    #overrules damage system in case of active block ability
    def take_damage(self, damage):
        if self.block_active:
            #calculates 50% chance that blockwill be applied
            if random.randint(0, 100) <= self.block_odds:
                final_damage = damage + random.randint(-2,2)
                final_damage_floor = max(final_damage, 0)
                #copied from damage calculation
                blocked_damage = final_damage_floor * (self.block_percent / 100)
                final_damage_floor -= blocked_damage
                #above lines takes blocked_damage for message, and subtracts the blocked damage from applied damage
                print(f"\n{self.name} blocks {blocked_damage} damage!")
                self.health = max(self.health - final_damage_floor, 0)
                print(f"\n{self.name} takes {final_damage_floor} damage! Health left: {self.health}")
            else:
                #otherwise refers to parent damage and notifies of failed block
                print(f"\n{self.name} failed to block!")
                super().take_damage(damage)
        else:
            #if not active, refers to parent function
            super().take_damage(damage)
        
    def heal_armour(self):
        #heal amount determined by subtracting current armour from Max
        #applies heal amount to get armour to max
        heal_amount = self.max_armour - self.armour
        self.armour += heal_amount
        print(f"\n{self.name} heals armour for {heal_amount}! Armour health: {self.armour}")



class Barbarian(Character):
    def __init__(self, name):
        super().__init__(name, health = 100, armour = 10, attack_power = 16, armour_attack_power = 4, evade_chance = 5, special_point_amount= 2)
        armour_break_active = False
        #default mode for ability set to fault
    def heal(self):
        super().heal(22)
        #heal amount for class
    #pull special works the same here
    def pull_specials(self):   
        print("1. Armour Break: Deals attack damage to enemy armour.")
        print("2. Beserk: Attack enemy with health damage and armour attack damage.")
        print("3. Go back.")
    def activate_special_one(self):
        #activates ability
        self.armour_break_active = True
        self.expend_special_point(1)
        self.attack_armour(wizard)
        #ability immediately applies attack
    def activate_special_two(self):
        #activates ability
        self.berserk_active = True
        self.expend_special_point(1)
        self.attack_health(wizard)
        #ability immediately applies attack
    #modifies attack)armour logic
    def attack_armour(self, opponent):
        #if armour break is active, attack damage is applied to enemy armour
        if self.armour_break_active == True:
            opponent.armour = max(0, opponent.armour - self.attack_power)
            print(f"\n{self.name} attacks {opponent.name} Armour for {self.attack_power} damage!")
            self.armour_break_active = False
            #single use ability, ability is set to false in this case
        else:
            super().attack_armour(opponent)
            #if ability not active refers to parent function
    #modifies attack health
    def attack_health(self, opponent):
        if self.berserk_active == True:
            effective_damage = max(0, self.attack_power + self.armour_attack_power - opponent.armour)
            #modifies damage calculation to be armour and health attack combined
            self.berserk_active = False
            #berserk attack is single use
        else: 
            effective_damage = max(0, self.armour_attack_power - opponent.armour)
        #Announce attempted Attack:
        print(f"\n{self.name} attacks {opponent.name} for {effective_damage} damage!")
        #Runs dodge Chance:
        if random.randint(0,100) <= opponent.evade_chance:
            print(f"\n{opponent.name} dodged the attack!")
            return
        else:
        #runs take damage with modified or unmodified effective damage
            opponent.take_damage(effective_damage)

class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health = 70, armour = 15, attack_power = 10, armour_attack_power = 6, evade_chance = 20, special_point_amount= 4)
    #abilities turned off by default
    fireball_active = False
    magic_mirror_odds = 50
    #heal amount higher for mage
    def heal(self):
        super().heal(26)
    #unique specials
    def pull_specials(self):   
        print("1. Fireball: Attack that deals 2X normal damage.")
        print("2. Magic Mirror(passive): Buff that adds chance to deflect damage back to attacker.")
        print("3. Go back.")
    def activate_special_one(self):
        self.fireball_active = True
        self.expend_special_point(1)
        self.attack_health(wizard)
        #ability is single use attack, activated immediately 
    def activate_special_two(self):
        self.expend_special_point(1)
        self.magic_mirror_active = True
        #ability is passive and lasts continuation of encounter

    def attack_health(self, opponent):
        # modified attack to account for fireball dealing 2x
        if self.fireball_active == True:
            effective_damage = max(0, (self.attack_power * 2) - opponent.armour)
            #same max clamp as normal. Doubles attack power. 
            print(f"\n{self.name} attacks {opponent.name} with fireball (2x attack boost) for {effective_damage} damage!")
            self.fireball_active = False
            #deactivates ability condition after use
            #continues to check dodge logic
            if random.randint(0,100) <= opponent.evade_chance:
                print(f"\n{opponent.name} dodged the attack!")
                return
            else:
                opponent.take_damage(effective_damage)
                #continues to take damage function with new effective damage value
        else: 
            super().attack_health(opponent)
            #if not active defaults to parent function

    def take_damage(self, damage):
        super().take_damage(damage)
        #function calls to parentand is largely the same
        #however, extra logic is applied. if player is damaged when magic mirror is active
        #there is a 50% chance that take damage function is applied to wizard for 5 damage
        #if ability does not get utilized program continues
        if self.magic_mirror_active == True:
            if random.randint(0,100) <= self.magic_mirror_odds:
                wizard.take_damage(5)
                return
            else:
                return
        else: 
            return

class Archer(Character):
    def __init__(self, name):
        super().__init__(name, health = 75, armour = 12, attack_power = 14, armour_attack_power = 4, evade_chance = 30, special_point_amount= 3)
    finesse_active = False
    agility_active = False
    agility_odds = 45
    #abilities set off by default. 
    #agility odds refers to dodge boost from ability (agility)
    #unique heal amount
    def heal(self):
        super().heal(22)
    #special abilities: archer
    #1. evade boost (evasion is doubled for three turns)
    #2. finesse (attack ignores armour)
    def pull_specials(self):   
        print("1. Agility (passive): Boosts chance to evade enemy attack.")
        print("2. Finesse: Attacks enemy health, ignoring armour, then does armour damage.")
        print("3. Go back.")
    def activate_special_one(self):
        self.agility_active = True
        self.expend_special_point(1)
    def activate_special_two(self):
        self.finesse_active = True
        self.attack_health(wizard)
        #if finesse is activated, modified attack_health is run
        self.attack_armour(wizard)
        #ability includes an armour attack follow up
        self.expend_special_point(1)
    
    def attack_health(self, opponent):
        #checks if finesse is active
        if self.finesse_active == True:
            effective_damage = max(0, self.attack_power)
            #if active, attack power ignores armour
            self.finesse_active = False
            #ability is then turned off(single use)
            #dodge chance is run
            if random.randint(0,100) <= opponent.evade_chance:
                print(f"\n{opponent.name} dodged the attack!")
                return
            else:
                opponent.take_damage(effective_damage)
                #take damage function runs with modified effective damage if dodge unssucesful
        else:
            super().attack_health(opponent)
        # if inactive, parent function runs as normal
    
    def take_damage(self, damage):
        #slightly modifies take damageif agility is active
        if self.agility_active == True:
            #agility active gives player an extra evasion roll
            #First agility roll happes in opponents attack_health function
            if random.randint(0,100) <= self.agility_odds:
                print(f"\n{self.name} dodged the attack thanks to Agility!")
                return
            #if this roll fails player takes damage
            else:
                super().take_damage(damage)
        else:
            #if ability not active, function refers to parent function
            super().take_damage(damage)

# EvilWizard class (inherits from Character)
class EvilWizard(Character):
    def __init__(self, name):
        super().__init__(name, health = 100, armour = 15, attack_power = 16, armour_attack_power = 3, evade_chance= 5, special_point_amount = 0)
    def heal(self):
        if self.health == self.max_health:
        #function does not bother running if at max health
        #this is unique to this class as character's are controlled by player 
        #whereas wizard is automatic
            pass
        else:
            super().heal(2)

def create_character():
    print("Choose your character class:")
    print("1. Warrior - High Armour and Moderate Attack. Low Evasion.")
    print("2. Barbarian - High Attack and High Health. Low Armour.")
    print("3. Mage - High Armour Attack and Extra Ability Points. Low Health.") 
    print("4. Archer - High Attack and High Evasion. Low Armour.")  
    #descriptions are given of gneral differences between playstyles
    class_choice = input("\nEnter the number of your class choice: ")
    
    name = input("\nEnter your character's name: ")
    #below logic provides for choice and accounts for error (defaults to warrior)
    if class_choice == '1':
        return Warrior(name)
    elif class_choice == '2':
        return Barbarian(name)
    elif class_choice == '3':
        return Mage(name)
    elif class_choice == '4':
        return Archer(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        return Warrior(name)
    
def battle(player, wizard):
    while wizard.health > 0 and player.health > 0:
    #loop runs as long as both player and boss have health value
        #stats are displayed at beginning of each turn in loop to allow player to strategize
        player.display_stats()
        wizard.display_stats()
        #menu
        print("\n--- Your Turn ---")
        print("1. Attack Armour")
        print("2. Attack Health")
        print("3. Use Special Ability")
        print("4. Heal")
        print("5. View Stats")
        print("6. Quit Game")

        choice = input("\nChoose an action: ")

        if choice == '1':
            player.attack_armour(wizard)
        elif choice == '2':
            player.attack_health(wizard)
        elif choice == '3':
            if player.special_points == 0:
                print("You are out of ability points. Returning to menu...")
                continue
                #continue skips player and wizard's turn, effectively returning to menu without breaking the battle loop
            else:
                player.pull_specials() #this statement pulls unique special descriptions regardless of character choice
                special_choice = input("\nChoose an action: ")
                if special_choice == "1":
                    player.activate_special_one()
                elif special_choice == "2":
                    player.activate_special_two()
                elif special_choice == "3":
                    continue
                #continue skips player and wizard's turn, effectively returning to menu without breaking the battle loop
                else:
                    #accounts for possibility of user inputting incorrectly
                    print("Invalid choice, returning to option menu.") 
                    continue
        elif choice == '4':
            player.heal()
        elif choice == '5':
            player.display_stats()
            wizard.display_stats()
        elif choice == '6':
            print("\nQuitting game...")
            break
        else:
            print("Invalid choice. Try again.")
        #below is AI logic so that Wizard will adjust behavior depending on armour level
        #this was preferable in my opinion to wizard only doing armour and then health
        #wizard ismore likely to attack armour the more armour player has. 
        #wizard will never attack armour if player has zero armour
        if wizard.health > 0:
            wizard.heal()
            if player.armour >= 15:
                if random.randint(0,100) <= 75:
                    wizard.attack_armour(player)
                else:
                    wizard.attack_health(player)
            elif 6 <= player.armour < 15:
                if random.randint(0,100) <= 50:
                    wizard.attack_health(player)
                else:
                    wizard.attack_armour(player)
            elif 1 <= player.armour < 6:
                if random.randint(0,100) <= 25:
                    wizard.attack_health(player)
                else:
                    wizard.attack_armour(player)
            else:
                wizard.attack_health(player)
        #condition for defeat
        if player.health <= 0:
            print(f"{player.name} has been defeated!")
            break
    #condition for victory
    if wizard.health <= 0:
        print(f"Congratulations! The wizard {wizard.name} has been defeated by {player.name}!")

#function which provides basic rules or game logic
def rules():
    print("\n---Rules---")
    print('"Player must defeat the Boss, the Evil Wizard."')
    print("Attack damage is within a range of + or - 2 of a character's attack power.")
    print('Armour blocks incoming damage. Damage done to player or wizard is "Attack Damage"-"Armour"')
    print("It is important to break an enemies Armour in order to increase attack effectiveness.")
    print("Special abilities consume 1 special ability point.")
    print("The game ends when the player or the boss reach 0 health.")

#this sequence has player select character, prints the rules, then initilizes battle loop
player = create_character()
wizard = EvilWizard("Final Boss")
rules()
battle(player,wizard)