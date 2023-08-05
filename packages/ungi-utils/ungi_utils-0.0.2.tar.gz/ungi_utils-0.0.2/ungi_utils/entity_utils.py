#!/usr/bin/env python3

import re
import spacy
import en_core_web_sm
nlp = en_core_web_sm.load()

def get_hashtags(input_string):
    """
    used to get #hastags from a inout string
    often you can find them in telegram chats
    """
    if len(input_string) > 0:
        hashtags = []
        r = re.compile("(#)+(\w{2,32})")
        for match in r.finditer(input_string):
            hashtags.append(match.group())
        return hashtags



def fix_up(str_in):
    """
    used to fix strings before being passed to the
    entity extractor
    """
    if str_in:
        no_ws = re.sub("\s+", " ", str_in)
        no_hashes = re.sub("(#)+(\w{2,32})", "", no_ws)
        no_hashes = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))', '', no_hashes, flags=re.MULTILINE)
        no_hashes = re.sub('[\S]+\.(net|com|org|info|edu|gov|uk|de|ca|jp|fr|au|us|ru|ch|it|nel|se|no|es|mil)[\S]*\s?','', no_hashes, flags=re.MULTILINE)
        clean = no_hashes.lower()

    return clean


def extract_ent(list_in):
    e_list = []
    e_list.append("test@gmail.com") #was a test will be removed
    for lst in list_in:
        doc = nlp(lst)
        for e in doc.ents:
            ent_d = {}
            ent_d["text"] = e.text
            ent_d["type"] = e.label_
            e_list.append(ent_d)
