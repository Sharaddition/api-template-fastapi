import modal
import pymongo
from pymongo import MongoClient

# Handles MongoDB to store paraphrase
cluster = MongoClient("mongodb+srv://najnar:najnar%400909@paraphrases.anbvazf.mongodb.net/?retryWrites=true&w=majority")

def store_pp(os, pp, tt, ml):
    db = cluster["paraphrases"]
    collection = db["list"]
    collection.insert_one({"os":os, "pp":pp, "tt":tt, 'ml': ml})


# Handles modal inference server for paraphrase generation
def paraphrase(model, sentence):
    if model == 'cpu':
        pp_fn = modal.Function.lookup("onnx-pp-cpu", "ParaphraseGenerator.run_inference")
    elif model == 'gpu':
        pp_fn = modal.Function.lookup("pp-gpu", "Generator.run_inference")
    else:
        pp_fn = modal.Function.lookup("pp-cpu", "Generator.run_inference")
    try:
        output = pp_fn.call(sentence)
        store_pp(sentence, output[0][0], output[1], model)
    except Exception as err:
        print(err)
    return output[0][0]