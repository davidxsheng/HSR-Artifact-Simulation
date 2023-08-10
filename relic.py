#%%
import numpy as np
import pandas as pd
import json
import os
import random
# %%
cd = os.getcwd()
# %%
class Relic():
    def __init__(self, source='cavern', set_name=None, piecetype=None, mainstat=None, substats=None, level=0):

        file_path = f'{cd}\mainstat_probability.json'
        with open(file_path) as f:
            self.mainstat_probability = json.load(f)
        file_path = f'{cd}\substat_probability.json'
        with open(file_path) as f:
            self.substat_probability = json.load(f)
        self.piecetype = piecetype
        if self.piecetype is None:
            if source == 'cavern':
                self.piecetype=random.choice(["Chest", "Boots", "Head", "Hands"])
            else: # source == 'SU'
                self.piecetype=random.choice(["Sphere", "Rope"])

        self.set_name = set_name
        if self.set_name is None:
            self.set_name = random.choice(['Good Set', 'Bad Set'])

        self.mainstat = mainstat
        if self.mainstat is None:
            self.roll_main()

        self.level=level

        self.substats = substats
        if self.substats is None:
            self.substats = {}
            if random.randint(0, 99) > 90: # 10% chance to have 4 substats
                num_subs = 4
            else: 
                num_subs = 3
            for i in range(num_subs):
                self.roll_sub()

    def roll_main(self):
        probabilities = self.mainstat_probability[self.piecetype]
        keys, values = zip(*probabilities.items())
        mainstat = random.choices(list(keys), list(values), k=1)
        self.mainstat = mainstat[0]
        return
    
    def roll_sub(self):
        temp_proba = self.substat_probability.copy()
        if len(self.substats) < 4:
            try:
                temp_proba.pop(self.mainstat) # Cannot roll main stat as substat
            except KeyError: # Mainstat doesn't exist in substat list
                pass
            for substat in self.substats.keys():
                temp_proba.pop(substat) 
            stat, weight = zip(*temp_proba.items())
            substat = random.choices(list(stat), list(weight), k=1)[0]
            self.substats[substat] = 1
        else:
            substat_to_level = random.choice(list(self.substats.keys()))
            self.substats[substat_to_level] += 1
        return
        
    def level_up(self):
        if self.level <= 15:
            self.level += 3
            self.roll_sub()
        else:
            raise Exception('Relic is max level already')
        return

    def score(self, criterion={'CR': 1, 'CDMG': 1, 'ATK%': 1, 'ATK': 0.3, 'SPD': 1}):
        score = 0
        for substat, num_rolls in self.substats.items():
            if substat in criterion:
                score += criterion[substat] * num_rolls
        return score

    def __str__(self) -> str:
        return f'{self.set_name}: {self.piecetype} lvl{self.level}\
            \n\t{self.mainstat}\n\t {self.substats}'
        


# %%
