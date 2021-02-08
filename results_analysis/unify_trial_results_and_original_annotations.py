# Purpose: The trial.csv results file does not include information about the trigger type, or other metadata that is
# tracked in the all_annotations_cleaned.jsonl file
# This script will produce a dataframe in which both types of information are present

import pandas as pd

df_trials = pd.read_csv("../results/02_judgments/trials.csv", encoding='unicode_escape')
df_annotations = pd.read_json("../experiments/stimuli/all_annotations_cleaned.jsonl", orient="records", lines=True)
df_annotations["sent_id"] = df_annotations["sent_id"].apply(str)
df_annotations = df_annotations.rename(columns={"sent_id": "id"}).set_index("id")
df_trials = df_trials.set_index("id")
df_unified = df_trials.join(df_annotations)
df_unified["id"] = df_unified.index