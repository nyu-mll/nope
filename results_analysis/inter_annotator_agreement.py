import krippendorff
import pandas as pd
import numpy as np

df = pd.read_csv("../results/02_judgments/trials.csv", encoding='unicode_escape')
my_df = df[["anon_id", "response", "id", "type"]]
my_df = my_df.set_index(["id", "type", "anon_id"])
my_df = my_df.unstack()

for condition in ["target-prior", "target-original", "target-negated", "filler"]:
    ratings_df = my_df.query(f"type == '{condition}'")
    ratings = np.array(ratings_df.transpose())
    print(condition + ": " + str(krippendorff.alpha(ratings)))


ratings = np.array(my_df.transpose())
print(krippendorff.alpha(ratings))