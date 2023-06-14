import re

# Checks if has HTML or not

def is_html(text):
    return re.search(r"<.*?>", text)


# Function to remove HTML tags leaving content

def remove_html_tags(text):
    clean_text = re.sub(r"<.*?>", "", text)
    return clean_text

# Function to split html and sentences

min_pp_len = 95     # Min text length to pp
def split_html(html):
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
                if len(html_list[index+1])<(min_pp_len/4):
                    if item[1] == 'h':
                        continue        # Skip Heading Tags
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


# Function to detect links in a sentrence

def has_link(text):
    pattern = r"\b(?:https?|http|ftp):\/\/\S+\b"
    has_url = re.search(pattern, text)
    return has_url