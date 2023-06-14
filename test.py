import re
import time
from threading import Thread

def executed(id):
    print('Executed:', id)

def delay_fn(sec):
    print('Thread:', sec)
    time.sleep(sec)
    executed(sec)

def compare_thread():
    start_time = time.time()
    thread1 = Thread(target=delay_fn, args=[4])
    thread2 = Thread(target=delay_fn, args=[3])
    thread1.start()
    thread2.start()
    delay_fn(2)
    thread1.join()
    thread2.join()
    print('Time Elapsed:', time.time()-start_time)
    # print(thread1, thread2, no_fn)

def split_html(html):
    pattern = re.compile(r'<[^>]+>|[^<]+')
    matches = pattern.finditer(html)

    html_list = []
    for match in matches:
        start = match.start()
        end   = match.end()
        html_list.append(html[start:end])
        # print('->',html[start:end])
    
    final_list, skip_next = [], False
    for index, line in enumerate(html_list):
        if not skip_next:
            if not is_html(line) and len(line) < 90:
                print(final_list[-1])
                print(line)
                print(html_list[index+1])
                try:
                    final_list[-2] = final_list[-2] + final_list[-1]
                    del final_list[-1]
                except:
                    pass
                final_list[-1] = final_list[-1] + line + html_list[index+1]
                print('==>', final_list[-1])
                skip_next = True
            else:
                final_list.append(line)
        else:
            skip_next = False

    return final_list

def remove_html_tags(text):
    clean_text = re.sub(r"<.*?>", "", text)
    return clean_text

def is_html(text):
    return re.search(r"<.*?>", text)

def has_link(text):
    pattern = r"\b(?:https?|http|ftp):\/\/\S+\b"
    has_url = re.search(pattern, text)
    return has_url

text = '<h2 alt="Bollywood News - Live Updates" title="Bollywood News - Live Updates" style="font-size: 0.9rem;">'
# print(has_link(text))
# htm = '<div class="tag-links"><strong>Tags : </strong> Ajav Devgn, Disney Hotstar, Disney Plus Hotstar, Kajol, News, OTT, OTT Platform, Remake, The Good Wife, The Trial, The Trial Pyaar Kanoon Dhoka, Trailer, Web Series, Web Show</div></div><h2 alt="Bollywood News - Live Updates" title="Bollywood News - Live Updates" style="font-size: 0.9rem;"><p>Catch us for latest Bollywood News, New Bollywood Movies update, Box office collection, New Movies Release , Bollywood News Hindi, Entertainment News, Bollywood Live News Today &amp; Upcoming Movies 2023 and stay updated with latest hindi movies only on Bollywood Hungama.</p></blockquote></div>'
htm = "<p>Shah Rukh Khan fans have been waiting for any and all updates about his next film <em>Jawaan</em>. The film will mark the superstar's first collaboration with director Atlee. On Monday, the actor answered some fan questions about the project during an Ask Me Answer session on Twitter and revealed some interesting details about the project. For instance, one fan asked, “Hello @iamsrk sir, what are your plans in evening? #AskSRK.” To this, SRK answered, “Was thinking will watch <em>Jawaan</em> with Atlee.” Does this mean the film is ready for release? Fans think so and are seemingly excited to witness the project unfold on the big screen.</p>"


# Catgeorises HTML, TEXT & Mixed Sentences
# for line in re.split(r'(?<!\d)\.(?!\d+\.|\s*<\/li>)', htm):
#     soup = BeautifulSoup(line, 'html.parser')
#     text = soup.get_text(separator=' ')
#     if text.strip() == '':
#         print('HTML:', line)
#     elif line.strip() != text.strip():
#         print('MIXD:', line)
#     else:
#         print('TEXT:',line)

# print(re.split(r'(?<!\d)\.(?!\d+\.|\s*<\/li>)', htm))

def split_html3(html):
    pattern = re.compile(r'<[^>]+>|[^<]+')
    matches = pattern.finditer(html)
    # Split HTML & TEXT
    html_list = []
    for match in matches:
        start = match.start()
        end   = match.end()
        html_list.append(html[start:end])
    # Remove silly HTML Tags
    for index, item in enumerate(html_list):
        if is_html(item) and not '/' in item[:2]:
            close_tag = item[:1]+'/'+item[1]
            try:
                if len(html_list[index+1])<23:
                    if item[1] == 'h':
                        # Skip Heading Tags
                        continue
                    elif close_tag == html_list[index+2][:3] or item[:2] == html_list[index+2][:2]:
                        del html_list[index+2]
                        del html_list[index]
            except:
                continue
    # Concat TEXT together
    final_list, raw_text = [], ''
    for item in html_list:
        if is_html(item):
            if raw_text:
                final_list.append(raw_text)
                raw_text = ''
            final_list.append(item)
        else:
            raw_text += item
    if raw_text:
        final_list.append(raw_text)
    return final_list

# html = []
# for line in re.split(r'(?<!\d)\.(?!\d+\.|\s*<\/li>)', htm):
#     html.append(line+'.')
# print(split_html2(html))

# htm = """"""

# for line in split_html3(htm):
#     print('->',line)
# print(split_html2(htm))

def create_article(raw_content):
    # 1. Clean the html
    texts = split_html3(raw_content)

    min_len = 95                  # Min text length to pp
    paraphrased_article = ''      # Final pp article
    for line in texts:
        pp_out = ''
        if len(line) >= min_len:
            # 2. Send quality sentences for paraphrasing
            if has_link(line):
                # 2.1 Check if contains any URL
                pp_out = line
                print('🏳️‍🌈', pp_out)
            else:
                # 2.2 Otherwise qualified for paraphrasing
                if is_html(' '.join(line.split())):
                    pp_out = line
                    print('⚠️', pp_out)
                else:
                    pp_out = ' '.join(line.split())
                    print('✔️', pp_out)
        else:
            # 2. Else return back poor qual lines.
            pp_out = line
            print('❌', pp_out)
        # 3. Append whatever good or bad line we got.
        paraphrased_article += pp_out
    # 4. Compile article & serve it
    return paraphrased_article

# create_article(htm)

text = """ <figure style="line-height:0;width:510px;height:340px" class="jsx-1647035624">"""

print(is_html(text))