from sentence_transformers import SentenceTransformer
import cohere
from tqdm import tqdm
import time
import numpy as np
import pickle

#device = 'cuda' # nvidia-gpu
# device = 'mps' # apple-gpu
device = 'cpu' # no gpu

f = open("cohere-key.txt", "r")

co = cohere.Client(f.read()) # or None if you dont want to use Cohere
model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2') # free offline transformer
def encode(text):
  if co is not None:
    if len(text) > 95:
      embed = []
      # prod key is 10000 per minute, free is 100. Cohere offers $300 in credits using htn2023
      sleep_time = 60 / 100
      k = 0
      start = time.time()
      for i in tqdm(range(0, len(text), 95)):
        embed += co.embed(texts=text[i:i + 95]).embeddings
        k += 1
        if k == 100:
          end = time.time()
          dur = end - start
          time.sleep(60 - dur if 60 - dur > 0 else 0)
          start = time.time()
          k = 0
    else:
      embed = co.embed(
          texts=text,
          model='embed-english-v2.0'
      ).embeddings
    embed = np.array(embed)
  else:
    embed = model.encode(text, device=device, show_progress_bar=True, batch_size=64)

  return embed


def runModel(input: str) -> int:
    with open('filename.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    
        encoded = encode([input])

        print(pipeline.predict(encoded.reshape(1, -1)))