#%%
from relic import Relic
import matplotlib.pyplot as plt
import numpy as np

# %%
def calc_score(loadout, criterion={'CR': 1, 'CDMG': 1, 'ATK%': 1, 'ATK': 0.3, 'SPD': 1}):
    score = 0
    for piecetype, relic in loadout.items():
        if relic is None:
            continue
        else:
            score += relic.score(criterion=criterion)
    return score
#
# %%
desired_main_stats = {
    'Head': 'HP',
    'Hands': 'ATK',
    'Chest': 'CR',
    'Boots': 'ATK%',
    'Sphere': 'Element%',
    'Rope': 'ATK%'
    }

num_trials = 100
trial_hist=[]
for trial in range(num_trials):
    loadout = {
        'Head': None,
        'Hands': None,
        'Chest': None,
        'Boots': None,
        'Sphere': None,
        'Rope': None
    }
    num_runs = 1000
    num_relics = num_runs * 2.1
    score_hist = []
    for i in range(int(num_relics)):
        new_relic = Relic()
        if new_relic.set_name == "Good Set": # Check if correct set
            if new_relic.mainstat == desired_main_stats[new_relic.piecetype]: # Check if correct main stat
                for j in range(5): #level it up to 15
                    new_relic.level_up()
                #print(new_relic.score())
                if (loadout[new_relic.piecetype] is None) or (new_relic.score(criterion={'CR': 1, 'CDMG': 1}) > loadout[new_relic.piecetype].score(criterion={'CR': 1, 'CDMG': 1})):
                    loadout[new_relic.piecetype] = new_relic
        score_hist.append(calc_score(loadout, criterion={'CR': 1, 'CDMG': 1}))
    trial_hist.append(score_hist)

results = np.percentile(np.stack(trial_hist, axis=0), q=[5, 25, 50, 75, 95], axis=0)
# %%
plt.figure(figsize=(10, 6))
plt.plot(results.T)
plt.grid()
plt.xlim(0, 2100)
plt.ylim(0, 30)
plt.xlabel('Relics Farmed')
plt.ylabel('Total Score')
plt.title('Relic Score from Cavern Relics at Various Percentiles')
plt.legend([5, 25, 50, 75, 95], title='Percentile')
# %%
for relic in loadout.values():
    print(relic)
# %%
