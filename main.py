import time
import logging
from flask import Flask, request
from handler import create_article
# from fastapi import FastAPI, Request

logging.basicConfig(filename="api.log",
                    format='%(asctime)s %(message)s',
                    filemode='w')

logger = logging.getLogger()
logger.setLevel(logging.INFO)

app = Flask(__name__)


@app.route('/', methods=['GET'])
def read_root():
    print(f'Hello at {time.time()}')
    return {"Hello": "World"}


@app.route('/', methods=['POST'])
def get_body():
    logger.info(">> New Post >>")
    start_time = time.time()
    # string_body = await request.body()
    # json_body   = await request.json()
    data = request.json
    if data.get('api_key') == "rfwerf":
        raw_text = data.get('text')
        logger.info(f"OG: {len(raw_text)} chars")
        pp_article = create_article(raw_text)
        logger.info(f"PP: {len(pp_article)} chars")
        ret_data   = {'code': 200, 'text': pp_article}
    else:
        print('API key not matched!')
        logger.warning("Someone else got API URL")
        ret_data = {'code': 404, 'text': 'API key not found in DB.'}
    total_time = str(time.time() - start_time)[:4]
    logger.info(f"TT: {total_time} secs.")
    return ret_data

# @app.get("/items/{item_id}")
# def read_item(item_id: int):
#     return {"item_id": item_id}

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=False)