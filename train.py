#!/usr/bin/env python3

import re
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np
import pickle
from infer import get_features


root_dir = Path(__file__).parent
data_dir = root_dir / "data"


def parse_file(file_path):
    """Read a file and return its text and text features."""

    with open(file_path) as file:
        file_text = file.read()

    return file_text, get_features(file_text)


def list_data():
    """Get lists of the files in the good and bad data directories"""
    return list(data_dir.glob("good/*")), list(data_dir.glob("bad/*"))


good_files, bad_files = list_data()

good_feature_vectors = np.array([
    parse_file(file_path)[1] for file_path in good_files
])
bad_feature_vectors = np.array([
    parse_file(file_path)[1] for file_path in bad_files
])

all_feature_vectors = np.concatenate([ good_feature_vectors, bad_feature_vectors ])
means = np.mean( all_feature_vectors, axis=0 )
stddevs = np.std( all_feature_vectors, axis=0 )

good_feature_vectors = np.nan_to_num( ( good_feature_vectors - means ) / stddevs )
bad_feature_vectors = np.nan_to_num( ( bad_feature_vectors - means ) / stddevs )

rng = np.random.default_rng()
rng.shuffle(good_feature_vectors)
rng.shuffle(bad_feature_vectors)

holdout = 1
x = np.concatenate([ good_feature_vectors[:-holdout], bad_feature_vectors[:-holdout] ])
y = np.array([ *[1 for _ in good_feature_vectors[:-holdout]], *[0 for _ in bad_feature_vectors[:-holdout]] ])

print("fitting model")

model = LogisticRegression(max_iter=100)
#model = RandomForestClassifier(n_estimators=10, random_state=42)
model.fit(x, y)

print("fitted model")

with open("model.pkl", "wb") as f:
    pickle.dump([means, stddevs, model], f)
