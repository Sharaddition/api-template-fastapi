import time
import modal
from threading import Thread
from pymongo import MongoClient

# Handles MongoDB to store paraphrase
cluster = MongoClient("mongodb+srv://najnar:najnar%400909@paraphrases.anbvazf.mongodb.net/?retryWrites=true&w=majority")

def store_pp(os, pp, tt):
    db = cluster["pbdb"]
    collection = db['cpu']
    collection.insert_one({"date":time.time(),"os":os, "pp":pp, "len":len(os),"tt":tt})


# Handles modal inference server for paraphrase generation
def paraphrase(sentence):
    pp_fn = modal.Function.lookup("pp-cpu", "Generator.run_inference")
    try:
        output = pp_fn.call(sentence)
        Thread(target=store_pp, args=[sentence, output[0][0], output[1]]).start()
    except Exception as err:
        output = [[sentence]]
        print('⚠️ Error:',err)
    return output[0][0]