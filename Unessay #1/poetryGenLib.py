#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3
# -*- coding: utf-8 -*-

# libraries getting used & commands to install them:
# (Since this is using python3, use pip3 to install packages)
# pip3 install urllib3
# pip3 install syllables
# (https://github.com/prosegrinder/python-syllables)
# pip3 install pronouncing
# pip3 install inflect

# Most of the words in the lists of JSON files of lots of words come from https://github.com/dariusk/corpora
# Which we talked about on that lab when we did poetry bots. I was pretty suprized when I found myself back there.

# Interestingly, after doing all of this work, writing all of this code, I'm not sure I've created a system that is
# all that much more powerful than the one we used to create our poetry bots originally. Heck, my sentence-formats.json
# is basically of the format that we used before to generate sentences before, it is just a bit more general, and
# the grammar logic in this file is just substancially more complex. Generally, this all just means that the poetry
# bot here generates grammatically correct (or almost grammatically correct) sentences that don't really make much sense
# or sound at all human. It definetly makes this poetry bot's poems sound interesting!

import inflect
import json
import pronouncing
import random
import re
import urllib3
import syllables

import indefiniteArticleLib

# Sory about all of the spaghetti code!
# I believe it is all relatively well commented though.

# API links & data files
dataMuseRequestAPI = 'api.datamuse.com/words'
sentenceJSONFile = 'sentence-formats.json'
givenSyllableCountFile = 'given-syllable-count.json'
verbsWithConjugationsFile = 'verbs_with_conjugations.json'
nounsFile = 'nouns.json'
personalNounsFile = 'personal_nouns.json'
adjsFile = 'adjs.json'

####################################### HELPERS #######################################

# returns False if the syntax is wrong, or returns the string, or an equivalent string 
# (if the given string is some accepted string like 'haiku')
def checkSyntax(str):
    # check if str matches a regular expression describing the input format
    if re.match('^([0-9]+[a-zA-Z]*,)*[0-9]+[a-zA-Z]*$', str):
        return str
    # check special cases
    elif str == 'haiku':
        return '5,7,5'
    elif str == 'limerick':
        return '8A,8A,6B,6B,8A'
    elif str == 'sonnet':
        return '10A,10B,10A,10B,10C,10D,10C,10D,10E,10F,10E,10F,10G,10G'
    # this was an invalid input
    else:
        return False


# Reads the file 'sentence-formats.json' and saves it as an object
def readJSON(file):
    with open(file) as jsonFile:
        return json.load(jsonFile)


# input is string described for generatePoem
# output is an object like so:
# {'poem': {
#     'lines': [['line1', 'words', ...], ['line2', 'words', ...], ...], <-- Each row will contain each word in the final poem
#     'wordType': [['a', 'noun-s', ...], ...] <-- Each word keeps track of the type of word that it is for sentence construction
#     'syllables': [[2, 1, ...], [2, 1, ...], ...], <-- Each number represents the number of syllables for the corresponding word
#     'syllableCount': [5, 7, 5, ...], <-- the total count of syllables per each line. Each row in the syllables table should 
#                                          sum up to a the corresponding number of this field
#     'rhymes': ['rhyme1', 'rhyme2', ...], <-- Each of these will contain a word used as a rhyme which can be indexed
#     'rhymesToLine': [0, 2, -1, 1, ...] <-- Each line points to the index of the word to rhyme to in the rhymes object.
#                                            If the index is negative, there it does not need to rhyme with anything.
# }}
# Used to parse the input string
def genPoemTemplate(desc):
    # split on commas
    vals = desc.split(',')
    # list of tuples of 
    pairs = [splitOnSyllable(line) for line in vals]

    # build poem object
    poem = {'lines':[], 'wordType':[], 'syllables':[], 'syllableCount':[], 'rhymes':[], 'rhymesToLine':[]}

    for p in pairs:
        poem['syllableCount'].append(int(p[0]))
        rhyme = p[1]

        if (rhyme == ''):
            # This line does not need to rhyme
            poem['rhymesToLine'].append(-1)
        else:
            if (rhyme not in poem['rhymes']):
                # The rhyme is new, so we add it to the rhymes list so we can find it later
                poem['rhymes'].append(rhyme)
            poem['rhymesToLine'].append(poem['rhymes'].index(rhyme))

    # clear the rhymes list
    for i in range(len(poem['rhymes'])):
        # mark that each rhyme should be reset
        poem['rhymes'][i] = '_'
    return poem


# helper for parsing the input format
def splitOnSyllable(pair):
    # the rhyme string
    rhyme = pair.lstrip('0123456789')
    # the number of syllables
    syllables = pair[:len(pair) - len(rhyme)]
    return syllables, rhyme

# checks if the word is actually a piece of grammar and not a real word
def isWordGrammar(word):
    grammars = ['.', '!', '?', ' ', ',', '-', '\n']
    return word in grammars

# returns the number of actual words in the sentence
def getLengthOfSentence(sentence):
    count = 0
    for word in sentence:
        # We need to skip words which are not actually words
        if not isWordGrammar(word):
            count += 1
    return count

# returns the number of words actual words left in the sentence
def getLengthOfRestOfSentence(sentence, sentenceIndex):
    return getLengthOfSentence(sentence[sentenceIndex:])



####################################### POEM GENERATOR CLASS #######################################

# Class for generating poems
class poemGenerator:

    # sets up all JSONs containing data used for generating poems
    def __init__(this):
        this.sentenceJSON = readJSON(sentenceJSONFile)
        this.givenSyllableCount = readJSON(givenSyllableCountFile)
        this.verbsWithConjunctions = readJSON(verbsWithConjugationsFile)
        this.nouns = readJSON(nounsFile)['nouns']
        #this.nouns = readJSON(personalNounsFile)['personalNouns']
        this.adjs = readJSON(adjsFile)['adjs']

        this.p = inflect.engine()

    # Generates a poem. The desc input is a string of comma seperated numbers and letters.
    # The number represents the number of syllables per line
    # The letter represents the rhyme scheme. Different letters are not garunteed to not rhyme
    # Each comma represents a new line
    # For example:
    #   '5,7,5' <- Haiku
    #   '10A,10A,10B,10B' <- Rhyming couplet
    #   '8A,8A,6B,6B,8A' <-Limerick
    #   '10A,10B,10A,10B,10C,10D,10C,10D,10E,10F,10E,10F,10G,10G' <- Shakespearean sonnet
    # The topics input is a list of strings which the generator will try to use as a topic for the poem
    # The output is a string containing the poem.
    def generatePoem(this, desc, topics):
        this.topics = topics
        this.poem = genPoemTemplate(desc)

        # this is used by functions to keep track of the sentence structure used thus far
        this.sentence = []
        this.sentenceIndex = 0
        this.countedSyllables = {}
        this.rhymeCollections = {}
        this.topicCollection = []
        this.plural = False;

        # fills in the topicCollections variable with words which are related to all of the topics
        this.generateRelatedWords()

        # generate each line of the poem.
        index = 0
        while(index < len(this.poem['syllableCount'])):
            if (this.generateLine(index)):
                index += 1

        # print the poem
        return this.printPoem()


    ####################################### LINE GENERATOR FUNCTIONS #######################################

    # Generates a line of the poem. Returns True if it succeeded, and False if it failed
    def generateLine(this, rowIndex):
        this.poem['lines'].append([])
        this.poem['syllables'].append([])
        this.poem['wordType'].append([])
        # If this is the last line, then the number of syllables must add up exactly!
        isLastLine = len(this.poem['syllableCount']) == (rowIndex + 1)

        maxRowSyllables = this.poem['syllableCount'][rowIndex]
        lineSyllables = 0 # The current number of syllables in this line
        while lineSyllables < maxRowSyllables or (this.sentenceIndex < len(this.sentence) and isWordGrammar(this.sentence[this.sentenceIndex])):
            if this.sentenceIndex >= len(this.sentence):
                # We need to generate a new sentence and append it to the end of the old sentence.
                # First we need to calculate the number of syllables left to generate in total as a hint to
                # give to the sentence format generator to ensure it doesn't try to generate a super long sentence.
                this.genSentenceTemplate(this.getSyllablesLeft())
                #print(this.getSyllablesLeft())
                #print(this.sentence)

            current = this.sentence[this.sentenceIndex]
            maximumSyllablesInLine = maxRowSyllables - lineSyllables
            wordsLeftInSentence = getLengthOfRestOfSentence(this.sentence, this.sentenceIndex)
            # Each of these functions returns a 2 tuple, (word, syllables)
            if current == 'the-subject':
                wordTuple = this.getSubject(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine)
            elif current == 'noun-s':
                wordTuple = this.getNoun(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine)
            elif current == 'noun-p':
                wordTuple = this.getNoun(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine, plural=True)
            elif current == 'verb-r':
                wordTuple = this.getVerb(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine)
            elif current == 'verb-ing':
                wordTuple = this.getVerb(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine, gerund=True)
            elif current == 'adj-r':
                wordTuple = this.getAdj(maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine)
            else:
                # The word is one which is already pre-defined.
                wordTuple = (current, this.countSyllablesOnWord(current))

            # Update the poem structure with new word
            this.poem['lines'][rowIndex].append(wordTuple[0])
            this.poem['syllables'][rowIndex].append(wordTuple[1])
            this.poem['wordType'][rowIndex].append(current)

            # Update our counters
            this.sentenceIndex += 1
            lineSyllables += wordTuple[1]
            this.updatePlurality(wordTuple[0], current)

        # look into if we should add a rhyme for the last word of this line:
        rhymeIndex = this.poem['rhymesToLine'][rowIndex]
        if rhymeIndex != -1 and this.poem['rhymes'][rhymeIndex] == '_':
            word = wordTuple[0]
            if isWordGrammar(word):
                word = this.poem['lines'][rowIndex][-2]
            this.poem['rhymes'][rhymeIndex] = word
            this.generateRhymes(word)
        return True


    # Generates a sentence template
    # takes in a maximum number of syllables to ensure the sentence will fit.
    # if allowAnySubject is set to true, this will accept things things like names easily
    # updates the this.sentence and this.sentenceIndex fields
    # returns the minumum number of syllables
    def genSentenceTemplate(this, maximumSyllables, allowAnySubject = False):
        while True:
            # generate initial sentence
            # If the maximum # of syllables is less than 3, it is extremely unlikely that a normal sentence will generate
            # with so few words in it, so we just generate interjections instead.
            if maximumSyllables < 3:
                wordList = this._genSentenceHelper('interjection', allowAnySubject)
            else:
                wordList = this._genSentenceHelper('sentence', allowAnySubject)
            # if there are definetly more syllables in wordlist than there are left in the poem, 
            # then we need to keep trying to generate another sentence
            if this.countSyllablesOfSentence(wordList) <= maximumSyllables:
                break

        # now, we do some post processing:
        # if 'verb-r' preceds 'verb-ing', replace 'verb-r' with 'am-are-is' for a cleaner sentence
        for i in range(1, len(wordList)):
            if wordList[i] == 'verb-ing' and wordList[i - 1] == 'verb-r':
                wordList[i - 1] == 'am-are-is'

        # replace 'am-are-is' with proper word based off word preceding it
        for i in range(1, len(wordList)):
            if wordList[i] == 'am-are-is':
                subject = wordList[i - 1]
                if subject == 'I':
                    wordList[i] = 'am'
                elif subject == 'you' or subject == 'they' or subject == 'noun-p':
                    wordList[i] = 'are'
                else:
                    wordList[i] = 'is'

        this.sentence.extend(wordList)
        return this.countSyllablesOfSentence(wordList)


    # Can regenerate the end of a sentence by using this function by looking for some part of a sentence instead of 'sentence' 
    def _genSentenceHelper(this, searchValue, allowAnySubject):
        # get the list of phrases
        strList = this.sentenceJSON[searchValue]

        # choose a random phrase from the list, and split it into a list of words
        wordList = random.choice(strList).split()

        index = 0
        maxIndex = len(wordList)
        while index < maxIndex:
            template = wordList[index][:1] == '#'
            theSubject = (not allowAnySubject) and (wordList[index] == 'the-subject')
            if template or theSubject:
                if (template):
                    # this is not a final word, we need to iterate again to find a word not starting with template symbol '#'
                    newWordList = this._genSentenceHelper(wordList[index][1:], allowAnySubject)
                else:
                    # this word is 'the-subject', except that we only want nouns as subjects, so we try again
                    newWordList = this._genSentenceHelper('subject', allowAnySubject)
                wordList = wordList[:index] + newWordList + wordList[index + 1:]
                maxIndex += len(newWordList) - 1
                index += len(newWordList)
            else:
                index += 1

        # the sentence has been cleaned up, so we can return the word list
        return wordList

    # This ensures that words updated correctly: 'I run', 'the farmer runs'
    def updatePlurality(this, currentWord, wordType):
        sentenceEnders = ['.', '!', '?']
        people = ['I', 'you', 'they', 'to']
        if currentWord in sentenceEnders or wordType == 'noun-s':
            this.plural = False
        elif currentWord in people or wordType == 'noun-p':
            this.plural = True



    ####################################### GET WORDS FUNCTIONS #######################################

    # This function is not currently getting used. If we were using it, it would be for adding specifics
    # into the sentences, like names or places.
    def getSubject(this, maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine):
        return ('Jack', 1)

    # Gets a noun!
    def getNoun(this, maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine, plural=False):
        if (isLastLine and wordsLeftInSentence > 1):
            # need to choose a word small enough that the other words can also appear on the line
            # give each word remaining at least 1 syllable
            maximumSyllablesInLine = max(maximumSyllablesInLine - wordsLeftInSentence, 1)   

        # Try to find a rhyming word
        rhymeIndex = this.poem['rhymesToLine'][rowIndex]
        if rhymeIndex != -1 and this.poem['rhymes'][rhymeIndex] != '_':
            # try to find a noun which rhymes if possible
            for rhyme in this.rhymeCollections[this.poem['rhymes'][rhymeIndex]]:
                if 'tags' in rhyme and 'n' in rhyme['tags'] and rhyme['numSyllables'] == maximumSyllablesInLine:
                    return (rhyme['word'], rhyme['numSyllables'])

        # usually try to find a word that fits the user's topics
        if len(this.topics) > 0 and random.random() >= 0.9:
            # get noun based on the topics
            for i in range(len(this.topicCollection)):
                if 'tags' in this.topicCollection[i] and 'n' in this.topicCollection[i]['tags'] and this.topicCollection[i]['numSyllables'] <= maximumSyllablesInLine:
                    word = this.topicCollection[i]['word']
                    syllables = this.topicCollection[i]['numSyllables']
                    # delete this value from the list so we don't keep seeing it pop up over and over again
                    del this.topicCollection[i]
                    if plural:
                        word = this.p.plural(word)
                        # need to recount the syllables because the number my have changed after making plural
                        syllables = this.countSyllablesOnWord(word)
                    return (word, syllables)

        # If we could not find a rhyme, just find a normal word.
        while(True):
            word = random.choice(this.nouns)
            if plural:
                word = this.p.plural(word)
            # If the word we found is valid, we can stop searching
            syllableCount = this.countSyllablesOnWord(word)
            if syllableCount <= maximumSyllablesInLine:
                break
        return (word, syllableCount)


    # Gets a verb!
    def getVerb(this, maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine, gerund=False):
        if (isLastLine and wordsLeftInSentence > 1):
            # need to choose a word small enough that the other words can also appear on the line
            # give each word remaining at least 1 syllable
            maximumSyllablesInLine = max(maximumSyllablesInLine - wordsLeftInSentence, 1)   

        # Try to find a rhyming word
        rhymeIndex = this.poem['rhymesToLine'][rowIndex]
        if rhymeIndex != -1 and this.poem['rhymes'][rhymeIndex] != '_':
            # try to get a verb based on the rhyme if possible
            for rhyme in this.rhymeCollections[this.poem['rhymes'][rhymeIndex]]:
                if 'tags' in rhyme and 'v' in rhyme['tags'] and rhyme['numSyllables'] == maximumSyllablesInLine:
                    return (rhyme['word'], rhyme['numSyllables'])

        # occasionally try to find a word that is related to the topic. This is more dangerous with verbs because
        # it is not very likely to conjugate correctly with the rest of the sentence.
        if len(this.topics) > 0 and random.random() >= 0.5:
            # get verb based on the topics
            for i in range(len(this.topicCollection)):
                if 'tags' in this.topicCollection[i] and 'v' in this.topicCollection[i]['tags'] and this.topicCollection[i]['numSyllables'] <= maximumSyllablesInLine:
                    word = this.topicCollection[i]['word']
                    syllables = this.topicCollection[i]['numSyllables']
                    # delete this value from the list so we don't keep seeing it pop up over and over again
                    del this.topicCollection[i]
                    return (word, syllables)

        # If we could not find a rhyme, just find a normal word.
        while(True):
            selection = random.choice(this.verbsWithConjunctions)
            if gerund:
                # This verb ends in 'ing'
                word = selection['gerund'][0]
            else:
                # This is just a normal verb
                word = selection['infinitive'][0]
                if not this.plural:
                    # The verb here should end in an s
                    if word[-1:] == 'y':
                        word = word[:-1] + 'ies'
                    elif word[-1:] == 'h':
                        word += 'es'
                    else:
                        word += 's'
            # If the word we found is valid, we can stop searching
            syllableCount = this.countSyllablesOnWord(word)
            if syllableCount <= maximumSyllablesInLine:
                break
        return (word, syllableCount)

    # Gets an adjective!
    def getAdj(this, maximumSyllablesInLine, rowIndex, wordsLeftInSentence, isLastLine):
        if (isLastLine and wordsLeftInSentence > 1):
            # need to choose a word small enough that the other words can also appear on the line
            # give each word remaining at least 1 syllable
            maximumSyllablesInLine = max(maximumSyllablesInLine - wordsLeftInSentence, 1)   

        # Try to find a rhyming word
        rhymeIndex = this.poem['rhymesToLine'][rowIndex]
        if rhymeIndex != -1 and this.poem['rhymes'][rhymeIndex] != '_':
            # try to find a noun which rhymes if possible
            for rhyme in this.rhymeCollections[this.poem['rhymes'][rhymeIndex]]:
                if 'tags' in rhyme and 'adj' in rhyme['tags'] and rhyme['numSyllables'] == maximumSyllablesInLine:
                    return (rhyme['word'], rhyme['numSyllables'])

        # usually try to find a word that fits the user's topics
        if len(this.topics) > 0 and random.random() >= 0.9:
            # get noun based on the topics
            for i in range(len(this.topicCollection)):
                if 'tags' in this.topicCollection[i] and 'adj' in this.topicCollection[i]['tags'] and this.topicCollection[i]['numSyllables'] <= maximumSyllablesInLine:
                    word = this.topicCollection[i]['word']
                    syllables = this.topicCollection[i]['numSyllables']
                    # delete this value from the list so we don't keep seeing it pop up over and over again
                    del this.topicCollection[i]
                    return (word, syllables)

        # If we could not find a rhyme, just find a normal word.
        while(True):
            word = random.choice(this.adjs)
            # If the word we found is valid, we can stop searching
            syllableCount = this.countSyllablesOnWord(word)
            if syllableCount <= maximumSyllablesInLine:
                break
        return (word, syllableCount)



    ####################################### DATAMUSE FUNCTIONS #######################################

    # Queries the DataMuse Api for words relating to our search
    # requestType is type of query, eg. rhy, nry, syn
    # search is the word we are directly using in our search
    # related is an array of related words
    # maximum is the maximum number of results, should not be set above 1000
    # Returns the JSON from DataMuse
    def doDMRequest(this, requestType, search, related = [], maximum = 500):
        http = urllib3.PoolManager()
        queryParams = {requestType: search, 'max': maximum, 'md': 'ps'}
        if related:
            queryParams['topics'] = related
      
        result = http.request('GET', dataMuseRequestAPI, queryParams)
        #print('completed DM request')
        return json.loads(result.data.decode('utf-8'))


    # Used to generate a list of words related to the topics
    def generateRelatedWords(this):
        # Do a query for means like for each of the topic words
        for topic in this.topics:
            this.topicCollection.extend(this.doDMRequest('ml', topic))


    # makes a new array of all of the words that rhyme, or nearly rhyme with some word
    def generateRhymes(this, word):
        # words that should be replaced, found by testing, because the API is slightly funky
        search = word
        replace = {'and':'sand', 'a-an':'an'}
        if word in replace:
            search = replace[word]
        # Possibly do 2 datamuse requests.
        # 1. Gets exact rhymes with topics set. If there are > 100, results stop
        # 2. Gets near rhymes with topics set.
        # all resulting values get put into one dictionary. These can be seperated using a filtering function
        rhymes = this.doDMRequest('rel_rhy', search, this.topics)
        if len(rhymes) <= 100:
            rhymes.extend(this.doDMRequest('rel_nry', search, this.topics))

        this.rhymeCollections[word] = rhymes




    ####################################### SYLLABLE FUNCTIONS #######################################

    # looks at the fields in this.poem and decides how many syllables are left in the poem in total
    def getSyllablesLeft(this):
        total = 0
        for i in range(len(this.poem['syllableCount'])):
            if (i >= len(this.poem['syllables'])):
                # We have not yet generated this row yet so we can just add the amount that should be in the row
                total += this.poem['syllableCount'][i]
            else:
                # We have already generated or started generating this row. If the sum of syllables is less than
                # the expected number of syllables, we have not yet finished generating this row.
                sumSyllables = sum(this.poem['syllables'][i])
                if (sumSyllables < this.poem['syllableCount'][i]):
                    # we add the sum of the syllables which have not yet been added
                    total += (this.poem['syllableCount'][i] - sumSyllables)
        return total


    # counts all of the syllables in some sentence (an array of words)
    def countSyllablesOfSentence(this, sentence):
        count = 0
        for w in sentence:
            count += this.countSyllablesOnWord(w)
        return count


    # counts the total number of syllables in a word
    def countSyllablesOnWord(this, word):
        if isWordGrammar(word):
            return 0
        elif word in this.givenSyllableCount:
            # the syllable is in my library of words that show up a lot.
            # It is important that this list contains a lot of words that show up often so we don't need to look up too many words
            return this.givenSyllableCount[word]
        elif word in this.countedSyllables:
            return this.countedSyllables[word]

        # Doing this look up is expensive, so we mostly want to avoid looking up words not in the givenSyllableCount dict
        pronunciation_list = pronouncing.phones_for_word(word)

        if (len(pronunciation_list) == 0):
            # The word is not in the pronounciation library, so we just estimate it
            count = syllables.estimate(word)
        else:
            # The word is in the pronounciation library, so we can use that to get an exact syllable count
            count = pronouncing.syllable_count(pronunciation_list[0])
        # keep a list of all words already looked up so we don't waste time looking up duplicates
        this.countedSyllables[word] = count
        return count


    ####################################### POEM PRINTING FUNCTIONS #######################################

    # Returns a string containing the entire poem
    def printPoem(this):
        #print(this.poem)

        full = []
        for row in this.poem['lines']:
            row.append('\n')
            full.extend(row)

        clean = this.cleanUpText(full)

        fullPoem = ''
        for word in clean:
            if isWordGrammar(word):
                fullPoem += word
            else:
                fullPoem += ' ' + word

        # Remove whitespace after new lines
        fullPoem = re.sub('\n ', '\n', fullPoem)

        return fullPoem[1:]


    # Does a final clean up of the text.
    def cleanUpText(this, sentenceList):
        uppercaseStrs = ['.', '!', '?', '\n']
        for i in range(len(sentenceList) - 1):
            if sentenceList[i] == 'a-an':
                if isWordGrammar(sentenceList[i + 1]) and (i + 2) < len(sentenceList):
                    sentenceList[i] = indefiniteArticleLib.indefinite_article(sentenceList[i + 2])
                else:
                    sentenceList[i] = indefiniteArticleLib.indefinite_article(sentenceList[i + 1])
        
        # iterate again so as not to mess up the last step
        sentenceList[0] = sentenceList[0].capitalize()
        for i in range(len(sentenceList) - 1):
            if sentenceList[i] in uppercaseStrs:
                sentenceList[i + 1] = sentenceList[i + 1].capitalize()

        return sentenceList



