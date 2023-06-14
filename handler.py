import regex
from ml import paraphrase
from threading import Thread


# Function to get Paraphrases from ML model

def rephrase(text):
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
    # 0. Clean the html
    texts = regex.split_html(raw_content)

    paraphrased_article = ''      # Final pp article
    for line in texts:
        pp_out = ''
        # 1. Trim the HTML tags
        if len(line) >= regex.min_pp_len:
            # 2. Send quality sentences for paraphrasing
            if regex.has_link(line):
                # 2.1 Check if contains any URL
                pp_out = line
            else:
                # 2.2 Otherwise qualified for paraphrasing
                if regex.is_html(' '.join(line.split())):
                    # 2.21 If is HTML than pass the sentence
                    pp_out = line
                else:
                    # 2.22 Qualified sentence for paraphrasing
                    pp_out = rephrase(' '.join(line.split()))
        else:
            # 2. Else return back poor qual lines.
            pp_out = line
        # 3. Append whatever good or bad line we got.
        paraphrased_article += pp_out
    # 4. Compile article & serve it
    return paraphrased_article