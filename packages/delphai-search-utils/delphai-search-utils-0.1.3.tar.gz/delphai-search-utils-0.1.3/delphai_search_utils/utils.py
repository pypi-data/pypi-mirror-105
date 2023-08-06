from sacremoses import MosesTruecaser
from os.path import join
from nltk.stem.snowball import SnowballStemmer
import logging
import nltk
from copy import deepcopy
from itertools import groupby
import json
import requests
import bson
from typing import Tuple, List, Generator
# get data path in a reproducible way
import os
this_dir, this_filename = os.path.split(__file__)
data_path = os.path.join(this_dir, "data")

mtr = MosesTruecaser(join(data_path, 'demonyms.truecasemodel'))

special_stopwords = ['compani', 'found',]
stemmer = SnowballStemmer(language='english')


def remove_conjunction(query_str: str) -> str:
    """ Removes conjunctions at the end of the query which are very likely
    not related to the actual query terms but just left overs from filters etc."""
    if len(query_str.strip()) == 0:
        return query_str
    pos_tags = nltk.pos_tag(nltk.word_tokenize(query_str))
    if not pos_tags:
        return query_str
    # iterate through pos tags and keep absolute string positions in mind
    for i, ((tok, pos), (_, pos_tag)) in enumerate(zip(split_with_indices(query_str), pos_tags)):
        if i == len(pos_tags) - 1 or is_masked(pos_tags[i + 1][0]):
            if pos_tag in ['CC', 'IN']:
                query_str = mask_substr(query_str, pos, pos + len(tok))
    return query_str


def remove_stopwords(query_str: str) -> str:
    # remove special_stopwords
    query_stops = [word for word in query_str.split() if stemmer.stem(word) in special_stopwords]
    for stop_word in query_stops:
        stop_index = query_str.index(stop_word)
        if stop_index >= 0:
            query_str = mask_substr(query_str, stop_index, stop_index + len(stop_word))
    return query_str


def is_masked(substring: str) -> bool:
    return (all(char == '_' for char in substring))


def remove_mask(query_str: str) -> str:
    """" Remove masked words;
    Doesn't guarantee that character indices stay the same afterwards,
    e.g. if masked words are removed in the middle of the query."""
    unmasked = query_str.replace('_', ' ')
    return ' '.join(unmasked.split())


def mask_substr(query_str: str, start_index: int, end_index: int) -> str:
    """ replaces the element between the given indices with underscores so that
    it is ignored for the subsequent filter detection; they are removed afterwards
    but kept for now to keep the correct character indices afterwards.
    This is not an ideal solution, so replacing it e.g. with a custom class which has
    a 'hide'-flag for each token would seem more resilient. (spaCy could do that..?)"""
    return query_str[:start_index] + '_' * (end_index - start_index) + query_str[end_index:]


def remove_elements_from_text(query_str: str, labels: List, remove_conjunctions=False) -> str:
    """ Removes the given labels from the query string and potentially also
    conjunctions; returns a cleaned query string."""
    for label in labels:
        query_str = mask_substr(query_str, label['start_index'], label['end_index'])
        if remove_conjunctions:
            query_str = remove_conjunction(query_str)
            query_str = remove_conjunction(query_str)
    return query_str


def add_label(labels, substring, label_type, start_ind, end_ind):
    labels.append({
        'start_index': start_ind,
        'end_index': end_ind,
        'substring': substring,
        'label_type': label_type
    })


def add_related_terms(elements, terms_dict, source, related_type):
    for original, terms in terms_dict.items():
        for term in terms:
            elements[related_type].append({
                'original': original,
                'term': term,
                'source': source,
            })


def add_to_log(changes_log, method, input_term, outputs):
    if changes_log is not None:
        # logging.info(f'adding {outputs} for {input_term} in {method}')
        changes_log[method].append({input_term: deepcopy(outputs)})


def truecase(query_str: str) -> str:
    """ (annoying) workaround to deal with multiple whitespaces etc."""
    truecased = query_str
    try:
        true_tokens = mtr.truecase(query_str, use_known=True)
        # returns list of tokens, re-assemble to proper string
        # with right amount of whitespaces etc.
        true_chars = ''.join(true_tokens)
        assembled = []
        true_index = 0
        for i, char in enumerate(query_str):
            if true_index < len(true_chars) and char.lower() == true_chars[true_index].lower():
                assembled.append(true_chars[true_index])
                true_index += 1
            else:
                assembled.append(char)
        truecased = ''.join(assembled)
    except Exception as exc:
        logging.warning(f'Exception in truecase() method: {exc}')
    return truecased


def api_wrap(api_info, request, max_timeouts=3, timeout_time=1.2):
    request_data = json.dumps(request)
    # Set the content type
    headers = {'Content-Type': 'application/json'}
    # If authentication is enabled, set the authorization header
    headers['Authorization'] = f'Bearer {api_info["key"]}'
    resp_raw = None
    while (resp_raw is None or resp_raw.text is None) and max_timeouts >= 0:
        try:
            resp_raw = requests.post(api_info["url"], request_data, headers=headers, timeout=timeout_time)
        except requests.exceptions.Timeout:
            logging.info(f'request to {api_url} timed out...')
        max_timeouts -= 1
    if resp_raw is None or resp_raw.text is None or resp_raw.status_code >= 400:
        return None
    else:
        return json.loads(resp_raw.text)


def is_object_id(term: str) -> bool:
    return bson.objectid.ObjectId.is_valid(term)


# https://stackoverflow.com/a/13734815
def split_with_indices(query: str, sep: str = ' ')\
        -> Generator[Tuple[str, int], None, None]:
    """ Splits the string by the given separator and returns all tokens
    together with their character start indices."""
    p = 0
    for k, g in groupby(query, lambda x: x == sep):
        q = p + sum(1 for i in g)
        if not k:
            yield query[p:q], p
        p = q
