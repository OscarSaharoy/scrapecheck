#!/usr/bin/env python3

import sys
import re
import pickle
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
import numpy as np


feature_getters = [
    lambda s: len(s), # number of characters
    lambda s: len(s.split()), # number of words
    lambda s: len(s.split("\n")), # number of lines
    lambda s: len(re.findall(r"[A-Z][a-z]", s)), # number of capitalised words
    lambda s: len(re.findall(r" [a-z]+", s)), # number of lowercase words
    lambda s: len(re.findall(r"((\. )|^| )[A-Z][A-Za-z0-9,\-–—'\"“”’;:() \[\]]{60,}(?=\.)", s, flags=re.MULTILINE)), # number of full sentences
    lambda s: sum(len(x[0]) for x in re.findall(r"(((\. )|^| )[A-Z][A-Za-z0-9,\-–—'\"“”’;:() \[\]]{60,})(?=\.)", s, flags=re.MULTILINE)), # number of characters within a sentence
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
    lambda s: len(re.findall(r'\b(according to|reported|said|told|announced|confirmed)\b', s, re.I)), # Attribution and sourcing
    lambda s: len(re.findall(r'\b(Monday|Tuesday|Wednesday|Thursday|Friday|Saturday|Sunday|yesterday|today|last week|this month)\b', s, re.I)), # Temporal references (news articles)
    lambda s: len(re.findall(r'\b(Mr\.|Ms\.|Dr\.|President|CEO|Director|Manager)\s+[A-Z][a-z]+', s)), # Professional titles and names
    lambda s: len(re.findall(r'[a-z],\s+[a-z][^.!?]{20,}[.!?]', s)), # Complex sentence structures with commas
    lambda s: len(re.findall(r'\b(analysis|research|study|report|according|evidence|significant|substantial)\b', s, re.I)), # Academic/formal language
    lambda s: len(re.findall(r'\b(began|started|continued|ended|during|throughout|since|until)\b', s, re.I)), # Storytelling elements
    lambda s: len(re.findall(r'[—;:]', s)), # Complex punctuation (em dashes, semicolons)
    lambda s: len(re.findall(r'\([^)]{10,}\)', s)), # Parenthetical information
    lambda s: len(re.findall(r'[^\w\s]', s)) / max(len(s.split()), 1), # High punctuation-to-word ratio (forms have lots of labels)
    lambda s: len(re.findall(r'[.!?]', s)) / max(len(re.findall(r'[A-Z][a-z]', s)), 1), # Sentence completion rate
    lambda s: len(re.findall(r'\n\s*\n[^\n]{100,}', s)), # Content density (articles have longer paragraphs)
    lambda s: len(re.findall(r'.+[.?!]\s*$', s, flags=re.MULTILINE)), # lines ending in punctuation
]


def get_features(s):
    text_features = [
        feature_getter(s) for feature_getter in feature_getters
    ]
    # divide each feature by character count and append to features
    text_features.extend([
        text_feature / len(s) for text_feature in text_features
    ])
    return np.array(text_features)


if __name__ == "__main__":
    with open("model.pkl", "rb") as f:
        [ means, stddevs, model ] = pickle.load(f)


    stdin = sys.stdin.read()
    features = np.array([ get_features(stdin) ])
    features = np.nan_to_num( ( features - means ) / stddevs )
    print(model.predict_proba(features)[0, 1])

