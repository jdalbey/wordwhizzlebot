
# Create a list of common english words from an external file
filename = "words_common.txt"
with open(filename) as f:
    content = f.readlines()
# remove whitespace characters like `\n` at the end of each line
content = [x.strip() for x in content]
wordlist = [s for s in content if len(s) >= 3]

# Given a list of strings, return the ones that are found in our dictionary
# @param a list of tuples, the first item is a string
def get_legal_words(candidate_list):
    legal_words = []
    # See if each candidate string is actually a dictionary word
    for candidate in candidate_list:
        word, route = candidate
        # If candidate string exists in our list of legal words
        if word in wordlist:
            # add it to results
            legal_words.append((word,route))
    return legal_words
