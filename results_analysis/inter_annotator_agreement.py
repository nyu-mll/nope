import krippendorff
import pandas as pd
import numpy as np
from pragmatics_dataset.results_analysis.unify_trial_results_and_original_annotations import df_unified

df = pd.read_csv("../results/02_judgments/trials.csv", encoding='unicode_escape')

def inter_annotator_agreement_breakdown(df, trigger=None):
    my_df = df[["anon_id", "response", "id", "type"]]
    my_df = my_df.set_index(["id", "type", "anon_id"])
    my_df = my_df.unstack()

    for condition in ["target-prior", "target-original", "target-negated", "filler"]:
        ratings_df = my_df.query(f"type == '{condition}'")
        ratings = np.array(ratings_df.transpose())
        alpha = krippendorff.alpha(ratings, level_of_measurement="interval")
        if np.isnan(alpha):
            continue
        print(condition + ": " + str(alpha))
        # if trigger == "clefts" and condition == "target-negated":
        #     print(ratings_df.to_string())

    ratings = np.array(my_df.transpose())
    print("overall: " + str(krippendorff.alpha(ratings, level_of_measurement="interval")))

for t in set(df_unified["trigger"]):
    if type(t) is not str:
        continue
    print("=" * 20)
    print(t)
    print("=" * 20)
    inter_annotator_agreement_breakdown(df_unified[df_unified["trigger"] == t], trigger=t)
    print()


print("=" * 20)
print("overall")
print("=" * 20)
inter_annotator_agreement_breakdown(df_unified)