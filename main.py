import time
from handler import create_article
from fastapi import FastAPI, Request
from ml import paraphrase

app = FastAPI()


@app.get("/")
def read_root():
    print(f'Hello at {time.time()}')
    return {"Hello": "World"}

@app.get("/test/")
def start_test():
    print('Starting paraphrase')
    output = paraphrase('cpu2',"Have 11 years' experience in print and digital media. Write on politics, defence and world affairs, and have a keen eye for human-interest stories.")
    return {"Paraphrase": output}

@app.post('/')
async def get_body(request: Request):
    # string_body = await request.body()
    json_body   = await request.json()
    if json_body['api_key'] == "rfwerf":
        pp_article = create_article(json_body['text'])
        print(json_body)
        ret_data = {'code': 200, 'text': pp_article}
    else:
        print('API key not matched!')
        ret_data = {'code': 404, 'text': 'API key not found in DB.'}
    return ret_data

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}