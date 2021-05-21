import pandas as pd
import os
import itertools

train = []
test = []
dev = []
for R in ["R1", "R2", "R3"]:
    for l, split in [(train, "train"), (test, "test"), (dev, "dev")]:
        df = pd.read_json(os.path.join("ANLI/anli_v1.0", R, f"{split}.jsonl"), orient="records", lines=True)
        df = df[["context", "hypothesis", "label"]]
        df = df.rename({"context": "sentence1", "hypothesis": "sentence2", "label": "gold_label"}, axis=1)
        df["gold_label"] = df["gold_label"].apply(lambda x: "entailment" if x=="e" else "neutral" if x=="n" else "contradiction")
        l.append(df)

for l, split in [(train, "train"), (test, "test"), (dev, "dev")]:
    df = pd.read_json(os.path.join("SNLI/snli_1.0", f"snli_1.0_{split}.jsonl"), orient="records", lines=True)
    df = df[["sentence1", "sentence2", "gold_label"]]
    l.append(df)

for l, split in [(train, "train"), (test, "dev_mismatched"), (dev, "dev_matched")]:
    df = pd.read_json(os.path.join("MultiNLI/multinli_1.0", f"multinli_1.0_{split}.jsonl"), orient="records", lines=True)
    df = df[["sentence1", "sentence2", "gold_label"]]
    l.append(df)

train = pd.concat(train)
test = pd.concat(test)
dev = pd.concat(dev)

if not os.path.exists("combined"):
    os.mkdir("combined")

for split, field in itertools.product([("train", train), ("test", test), ("dev", dev)], ["sentence1", "sentence2", "gold_label"]):
    field_short = "s1" if field=="sentence1" else "s2" if field=="sentence2" else "labels"
    with open(f"combined/{field_short}.{split[0]}", "w") as f:
        for line in list(split[1][field]):
            f.write(line.strip() + "\n")