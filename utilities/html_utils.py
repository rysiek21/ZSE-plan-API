import re

def get_text_between_tags(text: str, tag: str):
    start = text.find('<' + tag + '>')
    end = text.find('</' + tag + '>')
    return text[start + len(tag) + 2:end]

def get_text_between_tags_array(text: str, tag: str):
    possible_tags = re.findall(f'<{tag}([^>]*)>', text)
    texts = []
    for i in range(len(possible_tags)):
        first = text.find(possible_tags[i])
        closing = text.find(f'</{tag}>')
        texts.append(text[first + len(possible_tags[i])+1:closing])
        text = text[closing+3+len(tag):]
    return texts

def split_tag(text: str, tag: str):
    x = re.split(f'<{tag}([^>]*)>', text)
    for i in range(len(x)):
        x[i] = x[i].replace(f'</{tag}>', '')
    return x