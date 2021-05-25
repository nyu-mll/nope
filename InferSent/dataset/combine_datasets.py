import pandas as pd
import os
import itertools
import re

train = []
test = []
dev = []
# directory = "combined/data/build"
for R in ["r1", "r2", "r3"]:
    for l, split in [(train, "train"), (test, "test"), (dev, "dev")]:
        df = pd.read_json(os.path.join("anli", R, f"{split}.jsonl"), orient="records", lines=True)
        df = df[["premise", "hypothesis", "label"]]
        # df = df.rename({"context": "sentence1", "hypothesis": "sentence2", "label": "gold_label"}, axis=1)
        df["label"] = df["label"].apply(lambda x: "entailment" if x=="e" else "neutral" if x=="n" else "contradiction")
        df["source"] = f"ANLI_{R}"
        if split == "train":
            n_copies = 20 if R=="r2" else 10
            df = pd.concat([df.copy() for _ in range(n_copies)])
        # df = df[df["gold_label"].apply(lambda x: x in ["entailment", "contradiction", "neutral"])]
        l.append(df)

for l, split in [(train, "train"), (test, "test"), (dev, "dev")]:
    df = pd.read_json(os.path.join("snli", f"{split}.jsonl"), orient="records", lines=True)
    df = df[["premise", "hypothesis", "label"]]
    df["label"] = df["label"].apply(lambda x: "entailment" if x=="e" else "neutral" if x=="n" else "contradiction")
    df["source"] = "SNLI"
    l.append(df)

for l, split in [(train, "train"), (test, "test"), (dev, "dev")]:
    df = pd.read_json(os.path.join("fever_nli", f"{split}.jsonl"), orient="records", lines=True)
    df = df[["premise", "hypothesis", "label"]]
    df["label"] = df["label"].apply(lambda x: "entailment" if x=="e" else "neutral" if x=="n" else "contradiction")
    df["source"] = "FEVER"
    l.append(df)

for l, split in [(train, "train"), (dev, "mm_dev"), (dev, "m_dev")]:
    df = pd.read_json(os.path.join("mnli", f"{split}.jsonl"), orient="records", lines=True)
    df = df[["premise", "hypothesis", "label"]]
    df["label"] = df["label"].apply(lambda x: "entailment" if x=="e" else "neutral" if x=="n" else "contradiction")
    df["source"] = "MNLI"
    l.append(df)

train = pd.concat(train)
test = pd.concat(test)
dev = pd.concat(dev)

if not os.path.exists(f"combined"):
    os.mkdir(f"combined")

train.to_json(f"combined/train.jsonl", orient="records", lines=True)
test.to_json(f"combined/test.jsonl", orient="records", lines=True)
dev.to_json(f"combined/dev.jsonl", orient="records", lines=True)

for split, field in itertools.product([("train", train), ("test", test), ("dev", dev)], ["premise", "hypothesis", "label"]):
    field_short = "s1" if field=="hypothesis" else "s2" if field=="premise" else "labels"
    with open(f"combined/{field_short}.{split[0]}", "w") as f:
        for line in list(split[1][field]):
            f.write(re.sub(r"[\n\r]", " ", line) + "\n")
