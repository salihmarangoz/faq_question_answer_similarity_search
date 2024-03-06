import numpy as np
from sentence_transformers import SentenceTransformer

NUM_NEIGHBORS=5

documents = []
documents_raw = []
with open('data.txt', 'r') as f:
    entry = ""
    lines = f.readlines()
    for line in lines:
        if len(line.strip()) > 0:
            entry += line
        else:
            documents.append("<A>" + entry.strip())
            documents_raw.append(entry)
            entry = ""

model = SentenceTransformer('clips/mfaq', "en")
model.eval()
d_rep = model.encode(documents, batch_size=16)

while True:
    query = "<Q>" + input("Question: ") + "?"
    q_rep_i = model.encode([query])[0]

    scores = []
    for j, d_rep_i in enumerate(d_rep):
        score = q_rep_i @ d_rep_i.T
        scores.append(score)
    scores_sortidx = list(reversed(np.argsort(scores)))

    print("")
    for idx in range(NUM_NEIGHBORS):
        best_idx = scores_sortidx[idx]
        score = scores[best_idx]
        print("(*) FAQ ({}):".format(score), documents_raw[best_idx])
        print("")
    print("=============================================")
