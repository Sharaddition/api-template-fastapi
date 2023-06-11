import re
from ml import paraphrase
from threading import Thread

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
    # Create thread to simultaneously call all models 
    ml1 = Thread(target=paraphrase, args=['cpu',text])
    ml2 = Thread(target=paraphrase, args=['onnx',text])
    # Execute all models
    ml1.start()
    output = paraphrase('gpu',text)
    ml2.start()
    ml1.join()
    ml2.join()
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
            # 2. Else return back poor qual lines.
            pp_out = line
        # 3. Append whatever good or bad line we got.
        paraphrased_article += pp_out
    # 4. Compile article & serve it
    return paraphrased_article