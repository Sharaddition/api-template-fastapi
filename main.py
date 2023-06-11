import time
from ml import paraphrase
from flask import Flask, request
from handler import create_article
# from fastapi import FastAPI, Request

app = Flask(__name__)


@app.route('/', methods=['GET'])
def read_root():
    print(f'Hello at {time.time()}')
    return {"Hello": "World"}

# @app.route('/test', methods=['GET'])
# def start_test():
#     print('Starting paraphrase')
#     output = paraphrase('cpu2',"Have 11 years' experience in print and digital media. Write on politics, defence and world affairs, and have a keen eye for human-interest stories.")
#     return {"Paraphrase": output}

@app.route('/', methods=['POST'])
def get_body():
    # string_body = await request.body()
    # json_body   = await request.json()
    data = request.json
    if data.get('api_key') == "rfwerf":
        pp_article = create_article(data.get('text'))
        ret_data   = {'code': 200, 'text': pp_article}
    else:
        print('API key not matched!')
        ret_data = {'code': 404, 'text': 'API key not found in DB.'}
    return ret_data

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int("5000"), debug=False)