#!/usr/bin/env python3

import re
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np

root_dir = Path(__file__).parent.parent
data_dir = root_dir / "data"

feature_getters = [
    lambda s: len(s), # number of characters
    lambda s: len(s.split()), # number of words
    lambda s: len(s.split("\n")), # number of lines
    lambda s: len(re.findall(r"[A-Z][a-z]", s)), # number of capitalised words
    lambda s: len(re.findall(r" [a-z]+", s)), # number of lowercase words
    lambda s: len(re.findall(r"((\. )|^| )[A-Z][A-Za-z0-9,\-–—'\"“”’;:() \[\]]{60,}(?=\.)", s, flags=re.MULTILINE)), # number of full sentences
    lambda s: sum(len(x[0]) for x in re.findall(r"(((\. )|^| )[A-Z][A-Za-z0-9,\-–—'\"“”’;:() \[\]]{60,})(?=\.)", s, flags=re.MULTILINE)), # number of characters within a sentence
    lambda s: len(s) / len(s.split("\n")), # average line length
    lambda s: len(re.findall(r" but ", s)), # number of "but"
    lambda s: len(re.findall(r", [a-z]", s)), # number of commas followed by words
    lambda s: len(re.findall(r"^\s+[A-Za-z]+$", s, flags=re.MULTILINE)), # number of single-word lines
    lambda s: len(re.findall(r"subscribe|paywall|member|(sign(ed)?.?(up)|(in))|register|sorry|verify|access", s, flags=re.IGNORECASE)), # subscribe, paywall, sign up, login etc
    lambda s: len(re.findall(r" (be|a|in|not|have|that|it|with|he|she|as|you|do|at|this|his|her|by|from|say|said|or|an|will|one|all|would|there|what|so|if)[ ,.;]", s, flags=re.IGNORECASE)), # common words in prose count
    lambda s: len(re.findall(r"[£\–—‘’“” \-,;:?.'\"()\[\]/&%>$a-zA-Z0-9áéíÍñóú ]{300,}\n[£\–—‘’“” \-,;:?.'\"()\[\]/&%>$a-zA-Z0-9áéíÍñóú ]{300,}", s, flags=re.IGNORECASE | re.MULTILINE)), # paragraphs
    lambda s: len(re.findall(r'[.!?]\s+[A-Z][a-z]', s)),
    lambda s: len(re.findall(r'["“][^"”]{20,}"', s)),
    lambda s: len(re.findall(r'\b(however|meanwhile|but|after|since|when|while|although|despite)\b', s, flags=re.IGNORECASE)),
    lambda s: len(re.findall(r'\b\w+ed\b', s)),
    lambda s: len(re.findall(r'^\s*[A-Z][A-Za-z\s]{2,15}\s*$', s, flags=re.MULTILINE)),

    # Attribution and sourcing
    lambda s: len(re.findall(r'\b(according to|reported|said|told|announced|confirmed)\b', s, re.I)),

    # Temporal references (news articles)
    lambda s: len(re.findall(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|yesterday|today|last week|this month)\b', s, re.I)),

    # Professional titles and names
    lambda s: len(re.findall(r'\b(Mr\.|Ms\.|Dr\.|President|CEO|Director|Manager)\s+[A-Z][a-z]+', s)),

    # Complex sentence structures with commas
    lambda s: len(re.findall(r'[a-z],\s+[a-z][^.!?]{20,}[.!?]', s)),

    # Academic/formal language
    lambda s: len(re.findall(r'\b(analysis|research|study|report|according|evidence|significant|substantial)\b', s, re.I)),

    # Storytelling elements
    lambda s: len(re.findall(r'\b(began|started|continued|ended|during|throughout|since|until)\b', s, re.I)),

    # Complex punctuation (em dashes, semicolons)
    lambda s: len(re.findall(r'[—;:]', s)),

    # Parenthetical information
    lambda s: len(re.findall(r'\([^)]{10,}\)', s)),

    # High punctuation-to-word ratio (forms have lots of labels)
    lambda s: len(re.findall(r'[^\w\s]', s)) / max(len(s.split()), 1),

    # Sentence completion rate
    lambda s: len(re.findall(r'[.!?]', s)) / max(len(re.findall(r'[A-Z][a-z]', s)), 1),

    # Content density (articles have longer paragraphs)
    lambda s: len(re.findall(r'\n\s*\n[^\n]{100,}', s)),
]

def list_data():
    """Get lists of the files in the good and bad data directories"""
    return list(data_dir.glob("good/*")), list(data_dir.glob("bad/*"))

def parse_file(file_path):
    """Read a file and return its text and text features."""

    with open(file_path) as file:
        file_text = file.read()

    text_features = [
        feature_getter(file_text) for feature_getter in feature_getters
    ]
    # divide each feature by character count and append to features
    text_features.extend([
        text_feature / len(file_text) for text_feature in text_features
    ])
    
    return file_text, np.array(text_features)

good_files, bad_files = list_data()

good_feature_vectors = np.array([
    parse_file(file_path)[1] for file_path in good_files
])
bad_feature_vectors = np.array([
    parse_file(file_path)[1] for file_path in bad_files
])

score = 0
for _ in range(200):

    rng = np.random.default_rng()
    rng.shuffle(good_feature_vectors)
    rng.shuffle(bad_feature_vectors)

    all_feature_vectors = np.concatenate([ good_feature_vectors, bad_feature_vectors ])
    means = np.mean( all_feature_vectors, axis=0 )
    stddevs = np.std( all_feature_vectors, axis=0 )

    good_feature_vectors = np.nan_to_num( ( good_feature_vectors - means ) / stddevs )
    bad_feature_vectors = np.nan_to_num( ( bad_feature_vectors - means ) / stddevs )

    holdout = 7
    x = np.concatenate([ good_feature_vectors[:-holdout], bad_feature_vectors[:-holdout] ])
    y = np.array([ *[1 for _ in good_feature_vectors[:-holdout]], *[0 for _ in bad_feature_vectors[:-holdout]] ])

    print("fitting model")

    model = LogisticRegression(max_iter=100)
    #model = RandomForestClassifier(n_estimators=10, random_state=42)
    model.fit(x, y)

    print("fitted model")

    correct = sum(model.predict( good_feature_vectors[-holdout:] ))
    correct += sum( 1 - model.predict( bad_feature_vectors[-holdout:] ))
    correct_proportion = correct / (holdout * 2)
    print(correct_proportion)

    score += correct_proportion

print("score:", score / 200)
