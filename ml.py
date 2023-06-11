import modal
from threading import Thread
from pymongo import MongoClient

# Handles MongoDB to store paraphrase
cluster = MongoClient("mongodb+srv://najnar:najnar%400909@paraphrases.anbvazf.mongodb.net/?retryWrites=true&w=majority")

def store_pp(os, pp, tt, ml):
    db = cluster["paraphrases"]
    collection = db["list"]
    collection.insert_one({"os":os, "pp":pp, "tt":tt, 'ml': ml})


# Handles modal inference server for paraphrase generation
def paraphrase(model, sentence):
    if model == 'onnx':
        pp_fn = modal.Function.lookup("onnx-pp-cpu", "ParaphraseGenerator.run_inference")
    elif model == 'gpu':
        pp_fn = modal.Function.lookup("pp-gpu", "Generator.run_inference")
    elif model == 'cpu':
        pp_fn = modal.Function.lookup("pp-cpu", "Generator.run_inference")
    try:
        output = pp_fn.call(sentence)[0][0]
        Thread(target=store_pp, args=[sentence, output[0][0], output[1], model]).start()
    except Exception as err:
        output = [[sentence]]
        print('PP Error:',err)
    return output[0][0]