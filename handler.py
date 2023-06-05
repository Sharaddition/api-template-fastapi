import re
from ml import paraphrase
# Function to split html and sentences

def split_html(html):
    pattern = re.compile(r'<[^>]+>|[^<]+')
    matches = pattern.finditer(html)

    html_list = []
    for match in matches:
        start = match.start()
        end = match.end()
        html_list.append(html[start:end])

    return html_list


# Function to get Paraphrases from ML model

def send_to_pp(text):
    # Call thread to run in BG
    paraphrase('cpu',text)
    paraphrase('onnx',text)
    # Actual model output
    output = paraphrase('gpu',text)
    return output


# Manages the HTML and Text to create final article

def create_article(raw_content):
    # 1. Clean the html
    texts = split_html(raw_content)

    min_len = 95                  # Min text length to pp
    paraphrased_article = ''      # Final pp article
    for line in texts:
        if len(line) >= min_len:
            # 2. Send quality sentences for paraphrasing
            pp_out = send_to_pp(line)
        else:
            pp_out = line
            paraphrased_article += pp_out
    # Compile article & serve it
    return paraphrased_article