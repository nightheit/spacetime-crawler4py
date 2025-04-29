import heapq
import string
import sys
from simhash import Simhash
# import time

fingerprints_seen = []
stop_words = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "aren't", "as", "at",
    "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "can't", "cannot", "could", "couldn't",
    "did", "didn't", "do", "does", "doesn't", "doing", "don't", "down", "during", "each", "few", "for", "from", "further", "had",
    "hadn't", "has", "hasn't", "have", "haven't", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers",
    "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "isn't",
    "it", "it's", "its", "itself", "let's", "me", "more", "most", "mustn't", "my", "myself", "no", "nor", "not", "of", "off",
    "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "shan't", "she",
    "she'd", "she'll", "she's", "should", "shouldn't", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs",
    "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those",
    "through", "to", "too", "under", "until", "up", "very", "was", "wasn't", "we", "we'd", "we'll", "we're", "we've", "were",
    "weren't", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's",
    "with", "won't", "would", "wouldn't", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves"
}

# string.ascii_letters allows for tokenization on only alphanumeric English letters and string.digits allows for numbers 0-9. 
# Non English letters are treated as separators
# Source: https://stackoverflow.com/questions/16060899/alphabet-range-in-python

def tokenize(text: str) -> list[str]:
    english_letters = set(string.ascii_letters + string.digits + "'")
    tokenList = []
    currToken = []
    for character in text:
        # add valid chars to currToken
        if character in english_letters:
            currToken.append(character)
        else:
            # if the next char is invalid, save currToken, reset it, and continue
            if currToken:
                token = ''.join(currToken)
                if token not in stop_words:
                    tokenList.append(token.lower())
                currToken = []
    if currToken:
        token = ''.join(currToken)
        if token not in stop_words:
            tokenList.append(token.lower())
        currToken = []
    return tokenList


def computeWordFrequencies(tokens: list[str]) -> dict[str, int]:
    token_dict = {}
    for token in tokens:
        if token_dict.get(token, -1) != -1:
            token_dict[token] += 1
        else:
            token_dict[token] = 1
    return token_dict

def printFreq(token_dict: dict[str, int]) -> None:
    token_arr = []
    for token in token_dict:
        token_arr.append((token_dict[token], token))
    
    token_arr.sort(key=lambda x: x[0])

    # for i in range (len(token_arr) - 1, -1, -1):
    #     print(token_arr[i][1] + ' => ' + str(token_arr[i][0]))

    for i in range (len(token_arr)):
         print(token_arr[i][1] + ' => ' + str(token_arr[i][0]))
    print(len(token_dict))

def is_too_similar(url, tokens):
    fingerprint = Simhash(tokens).value
    curr_similar_fingerprints = 0
    for fingerprint_seen in fingerprints_seen:
        difference = fingerprint ^ fingerprint_seen
        # there is a fingerprint that is too similar, return True
        if difference.bit_count() <= 4:
            curr_similar_fingerprints += 1

        # allow for at most 2 similar sites
        if curr_similar_fingerprints >= 3:
            return curr_similar_fingerprints
        
    fingerprints_seen.append(fingerprint)
    # fingerprint is unique enough to add into set of seen fingerprints
    return curr_similar_fingerprints