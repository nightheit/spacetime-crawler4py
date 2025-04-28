import sys
ALPHANUM = set("""abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890'""")
STOPWORDS = {'','a', 'about', 'above', 'after', 'again', 'against', 'all', 'am', 'an', 'and', 'any', 'are', "aren't", 'as', 'at', 'be', 'because', 'been', 'before', 'being', 'below', 'between', 'both', 'but', 'by', "can't", 'cannot', 'could', "couldn't", 'did', "didn't", 'do', 'does', "doesn't", 'doing', "don't", 'down', 'during', 'each', 'few', 'for', 'from', 'further', 'had', "hadn't", 'has', "hasn't", 'have', "haven't", 'having', 'he', "he'd", "he'll", "he's", 'her', 'here', "here's", 'hers', 'herself', 'him', 'himself', 'his', 'how', "how's", 'i', "i'd", "i'll", "i'm", "i've", 'if', 'in', 'into', 'is', "isn't", 'it', "it's", 'its', 'itself', "let's", 'me', 'more', 'most', "mustn't", 'my', 'myself', 'no', 'nor', 'not', 'of', 'off', 'on', 'once', 'only', 'or', 'other', 'ought', 'our', 'ours\tourselves', 'out', 'over', 'own', 'same', "shan't", 'she', "she'd", "she'll", "she's", 'should', "shouldn't", 'so', 'some', 'such', 'than', 'that', "that's", 'the', 'their', 'theirs', 'them', 'themselves', 'then', 'there', "there's", 'these', 'they', "they'd", "they'll", "they're", "they've", 'this', 'those', 'through', 'to', 'too', 'under', 'until', 'up', 'very', 'was', "wasn't", 'we', "we'd", "we'll", "we're", "we've", 'were', "weren't", 'what', "what's", 'when', "when's", 'where', "where's", 'which', 'while', 'who', "who's", 'whom', 'why', "why's", 'with', "won't", 'would', "wouldn't", 'you', "you'd", "you'll", "you're", "you've", 'your', 'yours', 'yourself', 'yourselves'}


class Token:
    def __init__(self, d: str):
        self.data = d.lower()
    def __repr__(self):
        return self.data # for print
    def __eq__(self, o: ["Token",str]): #allows hashing and comparison to work between tokens
        if type(o) == Token:
            return self.data == o.data
        elif type(o) == str:
            return self.data == lower(o)
        else:
            raise TypeError(type(o))
    def __hash__(self): #allows Tokens to be in sets and dicts
        return hash(self.data)


class Frequencies:
    def __init__(self):
        self.freqs = dict() #dict of Token -> int
    def __add__(self, o: [Token, "Frequencies"]):
        if type(o) == Token: 
            if o in self.freqs.keys():
                self.freqs[o]+=1
            else:
                self.freqs[o]=1
            return self
        elif type(o) == type(self):
            ret = Frequencies()
            for key in o.freqs.keys():
                if key in ret.freqs.keys():
                    ret.freqs[key]+=o.freqs[key]
                else:
                    ret.freqs[key]=o.freqs[key]
            for key in self.freqs.keys():
                if key in ret.freqs.keys():
                    ret.freqs[key]+=self.freqs[key]
                else:
                    ret.freqs[key]=self.freqs[key]
            return ret
        else:
            raise TypeError(type(o))
    def __iadd__(self, o: "Frequencies"):
        self = self+o
    def __repr__(self): #allows for the default print() function to print the required format
        keyorder = sorted(sorted([k for k in self.freqs],key = lambda k: k.data), key = (lambda k: self.freqs[k]),reverse=True)
        return "\n".join([f"{k} -> {self.freqs[k]}" for k in keyorder])
    def total(self):
        ret = 0
        for key in self.freqs.keys():
            ret+=self.freqs[key]
        return ret


def tokenize(text: str) -> list[Token]: 
    ret = []
    word = [] 
    for char in text:
        if char in ALPHANUM: 
            word.append(char) 
        else:
            if word:
                ret.append(Token("".join(word))) #make new token from collected word
                word = []
    if word:
        ret.append(Token("".join(word))) # case for final word that ends the file
    return ret


def computeWordFrequencies(tokens: list[Token]) -> Frequencies: 
    freqs = Frequencies()
    for token in tokens:
        freqs + token # use the redefined add function as an insert
    return freqs


if __name__ == "__main__":
    freq = computeWordFrequencies(tokenize("Hello, my name is"))
    freq2 = computeWordFrequencies(tokenize("Name is Joe"))
    print(freq)
    print()
    print(freq2)
    print()
    print(freq+freq2)
    freq3 = freq+freq2
    print(freq3.total())