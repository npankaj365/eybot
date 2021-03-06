import random
import pickle
import copy
from utility import Utility


class MarkovModel:
    def __init__(self):
        self.corpus = {}

    """
    Create a dictionary of (key,value) pairs where key is n-gram configuration,
    from a file 
    """

    def read(self, filename, ngram=2):

        # Read contents from a file
        content = Utility.read_contents_from_file(filename)

        # Split contents into a list
        content = content.split()
        total_words = len(content) - ngram

        for word in range(total_words):
            # Set up key as tuples of n word grams
            key = tuple(i for i in content[word:word + ngram])
            # Append word to the value in (key,value) dictionary pair
            # Add new (key,value) pair if list does not exist
            if key in self.corpus:
                self.corpus[key].append(content[word + ngram])
            else:
                self.corpus[key] = [content[word + ngram]]


    """
    Obtain end of any given text based on position of last punctuation
    """
    def _get_eot(self, list_of_texts):

        eot_index = 0
        texts_size = len(list_of_texts) - 1

        for i in range(texts_size, 0, -1):
            # If puncuations, terminate here
            if list_of_texts[i][-1] in ['.','!','?']: 
                eot_index = i+1
                break
            elif list_of_texts[i][-1] in [',',';',':']:
                eot_index = i
                break
        return eot_index

    """
    Return text by appending words
    """

    def __get_text(self, n_length, words):

        resultant_text = []
        words_size = len(words) - 1

        # Contruct a text of size n words
        for ind in range(n_length):
            ngrams = tuple(words)

            # Capitalize solitary 'i'
            if words[0] == 'i': words[0].capitalize()
            
            resultant_text.append(words[0])

            # If words exist as key-words in corpus, shift by one word 
            # Then select random word from the list of words that follow key-words 
            if ngrams in self.corpus:
                words[:words_size] = words[1:words_size + 1]
                words[words_size] = random.choice(self.corpus[ngrams])

        resultant_text.append(words[words_size])

        # Capitalize first letter in resultant text
        resultant_text[0] = resultant_text[0].capitalize()
        
        # Obtain punctuation end
        end_of_text = self._get_eot(resultant_text)
        resultant_text = resultant_text[:end_of_text]

        return ' '.join(resultant_text)

    """
    Make sure initial words are contained in seed words if they exist
    """

    def __get_seedwords(self, seed_words, initials, w_c):
        if type(initials) in [str]:
            initials = [initials]

        while initials and len(initials) > 0:
            for i in range(len(self.corpus)):
                # If initial words are in word-components
                # Set seed words to be the word_components that contain initials
                if initials[0] in w_c[i] or (tuple(initials[0].split()) == w_c[i]):
                    seed_words = list(w_c[i])
                    initials = []
                    break
            if len(initials) > 0: initials.pop(0)

        return list(seed_words)

    """
    Generate a text of size n.
    """

    def generate_text(self, text_length, initials=['']):
        if not self.corpus: print('Corpus Empty')

        # Convert corpus dictionary into a list of word-components
        word_components = list(self.corpus)
        random.shuffle(word_components)

        # Get random integer to obtain one 'word component' to start resultant sentence
        rand_int = random.randint(0, len(list(self.corpus)))
        seed_words = word_components[rand_int]

        # Obtain seedwords from initials if they exist in the corpus
        seed_words = self.__get_seedwords(seed_words, initials, word_components)

        # Obtain resultant sentence of length n, commencing from seed words
        error = True
        while error:
            resultant_text = self.__get_text(text_length, seed_words)
            if resultant_text != '':
                error = False

        return resultant_text

    """
    Save the corpus using pickle
    """

    def save(self, filename):
        with open(filename, 'wb') as writer:
            pickle.dump(self.corpus, writer)

    """
    Load the saved pickle data
    """

    def load(self, filename):

        # Raise error if file does not exist
        if not Utility.check_integrity(filename):
            Utility.error('markov_model.load', 'File does not exist {0}'.format(filename))

        with open(filename, 'rb') as reader:
            data = pickle.load(reader)

        # Overwrite the corpus
        self.corpus = copy.deepcopy(data)

        del data
