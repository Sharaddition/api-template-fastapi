import regex
from ml import paraphrase
from threading import Thread


# Manages the HTML and Text to create final article

max_pp_len = 800
def create_article(raw_content):
    # 0. Clean the html
    texts = regex.split_html(raw_content)

    paraphrased_article = ''      # Final pp article
    for line in texts:
        pp_out = ''
        # 1. Trim the HTML tags
        line_len = len(line)
        if line_len >= regex.min_pp_len and line_len <= max_pp_len:
            # 2. Check if sentence is of appropriate length
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
                    pp_out = paraphrase((' '.join(line.split())).replace('"',"'"))
        else:
            # 2. Else return back poor qual lines.
            pp_out = line
        # 3. Append whatever good or bad line we got.
        paraphrased_article += pp_out
    # 4. Compile article & serve it
    return paraphrased_article