import json
import numpy as np 
import pandas as pd 
import tensorflow as tf
import tensorflow_hub as hub
from tensorflow import keras
from sklearn.metrics.pairwise import cosine_similarity
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')

n = 10
module_url = "https://tfhub.dev/google/nnlm-en-dim128/2"
embed = hub.KerasLayer(module_url)
lookup_media = pd.read_csv('resources/dataset/lookup.csv')

with open('resources/dataset/embedding_lookup.npy', 'rb') as f:
    lookup_matrix = np.load(f)

def serve_recommendations(audio_text):
	audio_text_embedding = embed([audio_text]).numpy()
	sim_vals = cosine_similarity(lookup_matrix, audio_text_embedding)
	sorted_sim_vals = np.argsort(sim_vals, axis=0)[::-1][:n]
	sorted_sim_vals = list(sorted_sim_vals.flatten())
	result_df = lookup_media[['artist', 'song']].iloc[sorted_sim_vals,:]
	parsed = json.loads(result_df.to_json(orient="records"))
	return json.dumps(parsed, indent=4) 

if __name__ == '__main__':
	audio_text = " A WHO KNOW NIGEL NG NEE SOON SO FAR SIR WHY IS THERE SUCH A POLICY MAY I ASK IF THERE ARE FAR \
	MORE HENCE THERE IS THERE A MILLION PER SE OR NO FINES ARE A CAR HE NEEDS A NEW ERA WHERE THERE ARE HIGHER THE \
	FOR NEARLY A YEAR SAW A MOTHER SHE WAS A RELIABLE A PIPED GAS SUCH AS I SAID EARLIER THE A YEAR HAD A WONDERFUL \
	NATIONAL THERE ARE CABINET A DAY WHERE THERE IS ILLEGAL THE BAY AREA WHERE PARTIES ARE GIVEN OUR LOWER WAGE \
	EARNERS I WILL DEAL WITH SOMEONE IS THE RATIONALE AS WELL AS THE LICENSEES IE GET A CAR WHEREAS THERE YOU \
	GATHER WHERE WE SEE WHETHER THERE ARE THERE IS A WILL THERE IS A ONCE THERE IS LESS OR BE A DAY WHERE MOH \
	AVA E JOHOR A YE SHI YI ZHONG YONG ASKED IF THERE IS A YEAR HE IS A FAIR SHARE IT WOULD THEY REQUIRE THEIR \
	ACRIMONY WITHIN THE CLUSTER IN A CARE FACILITY WHERE WE RECOGNISE THE WHERE SCREENING THESE ARE THE AGENCIES \
	THAT WE HAVE NO SAY I LOVE NO ONE MEASURE THERE ARE NO WHAT ARE OUR PLANS WERE ENERGY COSTS IN A UNKNOWINGLY \
	SIGNING LAWYER IN LESS BUSINESS THERE ARE STILL VERY MUCH A YEAR AGO THE DELAY THEIR FAMILY PARTIES FINANCE \
	CORE A MANUFACTURER SIR A ARE GOING THROUGH NOW AFTER EVERY LEADER IN THE FIELD WE ARE CLEARLY THERE IS A \
	SKILLS GAP YOU KNOW HOW DO THE VARIOUS A YEAR AND WILL LAY A SEMINAR PLAY A ROLE"
	print(serve_recommendations(audio_text))