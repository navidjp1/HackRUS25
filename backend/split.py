import re
from time import sleep
from obtain import extract_text_from_url


def get_body(text):

    start_match = re.search(r"START OF THE PROJECT GUTENBERG EBOOK", text, re.IGNORECASE)
    end_match = re.search(r"END OF THE PROJECT GUTENBERG EBOOK", text, re.IGNORECASE)
    if start_match and end_match:
        # Only use text in between
        #start = text[:start_match.start()]
        #end = text[end_match.end():]
        text = text[start_match.end():end_match.start()]

    return text


def count_alphanumeric(string):
  count = 0
  for char in string:
    if char.isalnum():
      count += 1
  return count    

def split_text(text, partition_size=5000):
    body = get_body(text)
    splits = re.split(r"(\r\n){3,}", body)
    cur_count = 0
    cur_part = ""
    partition = []
    for item in splits:
        cur_part += item
        count = count_alphanumeric(item)

        if count < 100:
           continue
        
        cur_count += count
        if cur_count > partition_size:
            partition.append(cur_part)
            cur_count = 0
            cur_part = ""

    return partition







