#%% 
import numpy as np
import pandas as pd
import json
import os
cd = os.getcwd()
#%%

df_ms = pd.read_csv(f"{cd}\mainstat_data_raw.csv")
totals = df_ms.groupby("Piece")['Count'].sum().reset_index(name='Sum')
df_ms = df_ms.merge(totals, on='Piece')
df_ms['Probability'] = df_ms.Count / df_ms.Sum

output = {}
for piece in df_ms["Piece"].unique():
    temp = df_ms.set_index("Piece").loc[piece, ["Mainstat", "Probability"]]
    try:
        temp = temp.to_frame().T
    except:
        pass
    temp = dict(zip(temp['Mainstat'], temp['Probability']))
    output[piece] = temp
json_output = json.dumps(output, indent=4)
with open("mainstat_probability.json", "w") as outfile:
    outfile.write(json_output)


df_ss = pd.read_csv(f"{cd}\substat_data_raw.csv")
df_ss['Probability'] = df_ss['Count'] / df_ss['Count'].sum()
ss_output = dict(zip(df_ss['Substat'], df_ss['Probability']))
json_output = json.dumps(ss_output, indent=4)
with open("substat_probability.json", "w") as outfile:
    outfile.write(json_output)


# %%
