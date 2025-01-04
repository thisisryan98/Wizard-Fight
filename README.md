# Wizard-Fight
Turn based boss battle, with character creation and unique classes.
RPG Boss Battle
A simple, console-based RPG where you (the player) must defeat the Evil Wizard in turn-based combat. Players can choose from various classes (Warrior, Barbarian, Mage, or Archer), each with distinct stats and special abilities. The Evil Wizard adapts its strategy based on the player’s armour.

Table of Contents
Features
Installation and Usage
Classes and Abilities
Gameplay Flow
How to Extend
License

Features
Four Playable Classes
Warrior: High armour, moderate attack, can block and restore armour.
Barbarian: High health and attack, can perform Armour Break and Berserk attacks.
Mage: Decent armour, specialized attacks (Fireball) and passive reflection (Magic Mirror).
Archer: High evasion, can boost dodge (Agility) and ignore armour (Finesse).
EvilWizard Boss
Dynamic strategy: Heals a small amount if not at max health and switches between attacking the player’s armour or health based on how much armour the player has.
Randomized Damage
All physical attacks vary by ±2 points from their stated damage, clamped to a minimum of 0 so you never deal negative damage.
Armour System
Damage to health is calculated as attack_power - opponent_armour (when greater than 0).
Breaking an opponent’s armour improves subsequent attacks.
Special Abilities
Each class has unique abilities consuming “special points.”
Single-use toggles or immediate attacks for strategic gameplay.
Turn-Based Battle Loop
Players pick from multiple options each turn: attack armour, attack health, use a special ability, or heal.
The wizard automatically heals and chooses whether to attack the player’s health or armour.
Victory Condition
Ends when either the player or the Evil Wizard reaches 0 health.

Installation and Usage
Requirements
Python 3.7 or higher (any version supporting random and f-strings is sufficient).
Download / Clone
Download this repository or copy the *.py file to your local machine.
Running the Game
In a terminal/command prompt, navigate to the folder containing the code.
Run:
bash
Copy code
python <filename>.py


Follow the on-screen prompts.
Selecting a Character
You will be asked to choose a class (1 for Warrior, 2 for Barbarian, etc.) and name your character.
Start the Battle
The game will display rules, then begin the battle loop.
Each turn, you can choose to attack armour, attack health, use special abilities, heal, or just check stats.

Classes and Abilities
1. Warrior
Stats: 80 HP, 20 Armour, 12 Attack Power.
Special Points: 2
Abilities:
Raise Shield: Toggle “block” mode (30% chance to halve incoming damage).
Restore Armour: Fully refill armour to max.
2. Barbarian
Stats: 100 HP, 10 Armour, 16 Attack Power.
Special Points: 2
Abilities:
Armour Break: Deal full attack power directly to the opponent’s armour.
Berserk: Combine normal attack power and armour attack power into a single large hit.
3. Mage
Stats: 70 HP, 15 Armour, 10 Attack Power, 6 Armour Attack Power.
Special Points: 4
Abilities:
Fireball: Double attack power (2x) against health.
Magic Mirror: 50% chance to reflect a portion of damage (5 HP) back to the attacker.
4. Archer
Stats: 75 HP, 12 Armour, 14 Attack Power.
Special Points: 3
Abilities:
Agility: Gain an extra dodge check when attacked (45% chance).
Finesse: Double attack, first attack hits health and ignores enemy armour, then second attack hits enemy armour.
5. EvilWizard (Non-playable Boss)
Stats: 100 HP, 15 Armour, 16 Attack Power.
AI: Automatically heals 2 HP if below max, then decides whether to strike the player’s armour or health based on the player’s current armour total.

Gameplay Flow
Character Creation
Input a class choice (1 to 4) and enter a name.
Rules
The program prints a brief summary of the rules and how damage/armour works.
Battle Loop
Each turn:
Show Stats: Player and Evil Wizard.
Player Action:
(1) Attack Armour
(2) Attack Health
(3) Use a Special Ability (if points remain)
(4) Heal (restores some HP, unique to your class)
(5) View Stats
(6) Quit game
Wizard Action (if alive):
Heals if not at max HP.
Attacks the player’s armour or health (AI logic based on armour amount).
End Condition
The battle ends when either the player or the Evil Wizard reaches 0 health.
Displays a victory or defeat message.

Ways to Expand
Add More Classes
Create new subclasses of Character, override the __init__, take_damage, attack_health, or attack_armour methods, and add new special abilities.
Additional Enemies
Instead of a single wizard, you could create multiple enemies or minibosses.
Pass references to the current opponent rather than using a globally named wizard.
Advanced AI
Modify the wizard’s logic to add conditions like “if player health < 20, always attack health” or new spells/abilities for the wizard.


Credits / Disclaimer
Author: Ryan Sullivan
Date: Jan 2025
This project is a learning exercise in Python OOP, turn-based game loops, and rudimentary AI. Use and modify freely for personal or educational purposes.
