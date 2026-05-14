import json
import time
import os
import random
from datetime import datetime

class Digimon:
    def __init__(self, name="Agumon"):
        self.name = name
        self.stage = "Rookie"  # Egg, Rookie, Champion, Ultimate
        self.hunger = 50
        self.happiness = 50
        self.energy = 80
        self.strength = 30
        self.age = 0
        self.last_time = time.time()
        self.ascii = self.get_ascii()

    def get_ascii(self):
        if self.stage == "Egg":
            return "   \n ( )\n/___\\"
        elif self.stage == "Rookie":
            return " /\\_/\\ \n( o.o ) \n > ^ < "
        elif self.stage == "Champion":
            return " /\\_/\\ \n( o.o ) \n > ^ < \n  / \\"
        else:
            return " /\\_/\\ \n( o.o ) \n > ^ < \n /   \\ \n|     |"

    def update(self):
        now = time.time()
        delta = int(now - self.last_time)
        self.last_time = now
        decay = delta // 60 + 1  # decay every ~60s simulated
        self.hunger = max(0, self.hunger - decay * 2)
        self.happiness = max(0, self.happiness - decay)
        self.energy = max(0, self.energy - decay)
        self.age += delta // 300  # age up every 5 min simulated

        # Evolution checks
        if self.stage == "Egg" and self.happiness > 40 and self.hunger > 30:
            self.stage = "Rookie"
            print(f"\n🎉 {self.name} hatched into Rookie stage!")
        elif self.stage == "Rookie" and self.strength > 50 and self.happiness > 70:
            self.stage = "Champion"
            print(f"\n🔥 {self.name} evolved to Champion!")
        self.ascii = self.get_ascii()

    def feed(self):
        self.hunger = min(100, self.hunger + 25)
        self.happiness = min(100, self.happiness + 10)
        print(f"🍖 Fed {self.name}. Hunger restored!")

    def play(self):
        if self.energy < 20:
            print("Too tired to play!")
            return
        self.happiness = min(100, self.happiness + 25)
        self.strength = min(100, self.strength + 15)
        self.energy = max(0, self.energy - 20)
        print(f"⚔️ Played with {self.name}. Strength up!")

    def rest(self):
        self.energy = min(100, self.energy + 40)
        self.hunger = max(0, self.hunger - 10)
        print(f"💤 {self.name} rested.")

    def battle(self):
        if self.energy < 30 or self.hunger > 70:
            print("Too weak to battle!")
            return
        win_chance = (self.strength + self.happiness) / 2
        if random.randint(1, 100) < win_chance:
            self.strength = min(100, self.strength + 20)
            self.happiness = min(100, self.happiness + 15)
            print(f"🏆 {self.name} won the battle!")
        else:
            self.happiness = max(0, self.happiness - 20)
            print(f"{self.name} lost... but learned from it.")

    def status(self):
        self.update()
        print("\n" + "="*40)
        print(f"📟 DIGIVICE - {self.name} ({self.stage})")
        print(self.ascii)
        print(f"Age: {self.age//60}h {self.age%60}m")
        print(f"Hunger: {self.hunger}/100   Happiness: {self.happiness}/100")
        print(f"Energy: {self.energy}/100    Strength: {self.strength}/100")
        print("="*40)

def load_or_new():
    if os.path.exists("digimon_save.json"):
        with open("digimon_save.json", "r") as f:
            data = json.load(f)
            digi = Digimon(data["name"])
            digi.stage = data["stage"]
            digi.hunger = data["hunger"]
            digi.happiness = data["happiness"]
            digi.energy = data["energy"]
            digi.strength = data["strength"]
            digi.age = data["age"]
            digi.last_time = time.time()
            return digi
    return Digimon()

def save(digimon):
    data = {
        "name": digimon.name,
        "stage": digimon.stage,
        "hunger": digimon.hunger,
        "happiness": digimon.happiness,
        "energy": digimon.energy,
        "strength": digimon.strength,
        "age": digimon.age
    }
    with open("digimon_save.json", "w") as f:
        json.dump(data, f)
    print("💾 Progress saved!")

def main():
    print("🔴 DIGIVICE ACTIVATED 🔴")
    digi = load_or_new()
    while True:
        digi.update()
        print("\n1. Status  2. Feed  3. Play/Train  4. Rest  5. Battle  6. Save & Quit")
        choice = input("Choose action: ").strip()
        if choice == "1":
            digi.status()
        elif choice == "2":
            digi.feed()
        elif choice == "3":
            digi.play()
        elif choice == "4":
            digi.rest()
        elif choice == "5":
            digi.battle()
        elif choice == "6":
            save(digi)
            print("See you next time, Tamer!")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
