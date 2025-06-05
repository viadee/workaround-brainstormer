from sentence_transformers import  SentenceTransformer, util

workarounds = [
"As a receptionist, when specialist availability is limited, I keep a separate informal list of potential cancellation or emergency slots to offer patients faster alternatives without waiting for the official system update",
"As a receptionist, when confirmation calls or texts cannot be delivered due to communication barriers, I ask family members or emergency contacts for alternative ways to confirm appointments and reduce no-shows.",
"As a receptionist, when patients provide incomplete or unclear insurance information, I call the insurance provider directly during the scheduling call to quickly verify coverage and reduce appointment cancellations."
]

model = SentenceTransformer('T-Systems-onsite/cross-en-de-roberta-sentence-transformer')

embeddings = model.encode(workarounds, convert_to_tensor=True)

similarity_matrix = util.pytorch_cos_sim(embeddings, embeddings)

import numpy as np
sim_array = similarity_matrix.cpu().numpy()
avg_similarity = (np.sum(sim_array) - np.trace(sim_array)) / (len(workarounds)**2-len(workarounds))

print(f"Avg: {avg_similarity:.4f}")
print(f"Sem: {1- avg_similarity:.4f}")