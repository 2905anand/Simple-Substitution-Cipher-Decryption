# Write your script here
# import csv
import copy

# csvFile = "/unigram_freq copy.csv"

wordsWithOccurence = {}

# print(f"There are {len(words)} words.")
EnglishWordswithPattern = {}

# possibleLetterMappings = {'a':[],'b':[],'c':[],'d':[],'e':[],'f':[],'g':[],'h':[],'i':[],'j':[],'k':[],'l':[],'m':[],'n':[],'o':[],'p':[],'q':[],'r':[],'s':[],'t':[],'u':[],'v':[],'w':[],'x':[],'y':[],'z':[]}
possibleLetterMappings = {}
letters = []
cipherWords = []

def main(ciphertext):

    dictionary = {}
    length = len(ciphertext) 

    cleanedCiphertext = cleanCipher(ciphertext)
    
    for letter in cleanedCiphertext:
        if letter not in letters and letter != ' ':
            letters.append(letter)
    # print(letters)

    createEmptyMapping(letters)

    

    for key in wordsWithOccurence:
        EnglishWordswithPattern[key] = generateWordPattern(str(key))

    cipherWords = cleanedCiphertext.split(" ")
    cipherWordsFrequency = {}

    cipherWordsFrequency = findingFrequency(cipherWords)

    wordSizeFreq = wordFrequency(cipherWords)
    sortedWordSizeFreq = dict(sorted(wordSizeFreq.items(), reverse = True))

    lettersFreq = letterFrequency(cleanedCiphertext)

    sortedLettersFreq = dict(sorted(lettersFreq.items(), key=lambda item: item[1], reverse=True))

    intersectMap = createEmptyMapping(letters)
    for word in cipherWords:
        map = createEmptyMapping(letters)

        pattern = generateWordPattern(word)
        if pattern not in allPatterns:
            continue

        for candidate in allPatterns[pattern]:
            assignMappings(map, word, candidate)
    
        intersectMap = intersectMappings(intersectMap, map)
    
    for key, values in intersectMap.items():
        list = []
        for value in values:
            list.append(value.lower())
        intersectMap[key] = list

    return removeMappedSolvedLetters(intersectMap)

def intersectMappings(firstMap, secondMap):
    intersectedMap = createEmptyMapping(letters)
    for letter in letters:
        if firstMap[letter] == []:
            intersectedMap[letter] = copy.deepcopy(secondMap[letter])
        elif secondMap[letter] == []:
            intersectedMap[letter] = copy.deepcopy(firstMap[letter])
        else:
            for mappedLetter in firstMap[letter]:
                if mappedLetter in secondMap[letter]:
                        intersectedMap[letter].append(mappedLetter)
    
    return intersectedMap

def decrypt(finalMappings, ciphertext):
    leter = ""
    for i in letters:
        leter += i
    
    key = {}
    for s in leter:
        if len(finalMappings[s]) == 1:
            key[s] = finalMappings[s][0]
        else:
            key[s] = "_"

    return decryptMessage(key, ciphertext), key

def decryptMessage(key, ciphertext):
    plaintext = ""
    for letter in ciphertext:
        if letter in [',','.',' ',';','!']:
            plaintext+=letter
        else:
            plaintext+=key[letter]
    
    return plaintext

def createEmptyMapping(letters):
    emptyMapping = {}
    for letter in letters:
        emptyMapping[letter] = []
    return emptyMapping

def removeMappedSolvedLetters(resolvedMappings):
    loop = True
    while loop:
        solvedLetters = []
        loop = False
        
        for letter in letters:
            if len(resolvedMappings[letter]) == 1:
                solvedLetters.append(resolvedMappings[letter][0])
        
        for letter in letters:
            for s in solvedLetters:
                if len(resolvedMappings[letter]) != 1 and s in resolvedMappings[letter]:
                    resolvedMappings[letter].remove(s)
                    if len(resolvedMappings[letter]) == 1:
                        loop = True
    return resolvedMappings


    
def generateWordPattern(word):
    pattern = ""
    counter = 0
    d = {}
    set1 = set()
    for i in word:
        if i in d:
            pattern =pattern + "." + str(d[i])
        else:
            d[i] = counter
            pattern =pattern + "." + str(d[i])
            counter+=1
    
    return pattern[1:]

def findingFrequency(words):
    frequency = {}
    for word in words:
        if word in frequency:
            frequency[word] +=1
        else:
            frequency[word] = 1
    return frequency

def wordFrequency(words):
    wordFreq = {}
    for word in words:
        if len(word) in wordFreq:
            wordFreq[len(word)].append(word)
        else:
            wordFreq[len(word)] = [word]
    return wordFreq

def letterFrequency(ciphertext):
    lettersFreq = {}
    for s in ciphertext:
        if s in lettersFreq:
            lettersFreq[s]+=1
        else:
            lettersFreq[s] = 1
    return lettersFreq

def cleanCipher(ciphertext):
    cleanedCiphertext = ""
    for s in ciphertext:
        if s in [',','.','!',';']:
            continue
        cleanedCiphertext +=s
    return cleanedCiphertext 


def assignMappings(letterMappings, word, key):
    for i in range(len(key)):
        lower_key = key[i].lower()
        if key[i] not in letterMappings[word[i]]:
            letterMappings[word[i]].append(key[i])

def match(word):
    for key in EnglishWordswithPattern.keys():
        key = str(key)
        
        if len(key) == len(word):
            count = 0
            s = ""
            for i in range(len(word)):
                if key[i] != word[i]:
                    count += 1
                    s = key
            if count == 1:
                return s
    return " "


class DecipherText(object): # Do not change this
    def decipher(self, ciphertext): # Do not change this
        """Decipher the given ciphertext"""

        # Write your script here
        finalMappings = main(ciphertext)
        # print(finalMappings)

        final = createEmptyMapping(letters)
        s = []
        for key, values in finalMappings.items():
            if len(values) == 1:
                final[key] = values
                s.append(finalMappings[key][0])
            else:
                for value in values:
                    if value not in s:
                        final[key].append(value)
    
        # print(final)
        # print(s)
        alphabets = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']
        unmapped = []
        for letter in alphabets:
            if letter not in s:
                unmapped.append(letter)
    
        # print(unmapped)

        msg, key = decrypt(finalMappings, ciphertext)
        # print(key)
    
        msg = cleanCipher(msg)
        msg = msg.split()
        
        # print(msg)
        cleanedCiphertext = cleanCipher(ciphertext)
        cipherWords = cleanedCiphertext.split(" ")
        for word in msg:
            s = match(word)
        
            if s!=" ":
                for i in range(len(msg)):
                    if(msg[i] == word):
                    # print(cipherWords[i]," ",word)
                        break
                # print(s," ",word)
                if word not in EnglishWordswithPattern.keys():
                    # print(word)
                    for j in range(len(word)):
                        if(word[j] == '_'):
                            key[cipherWords[i][j]] = s[j]
                        elif (word[j] != s[j]):
                            key[cipherWords[i][j]] = s[j]

    
        # print("\n")
        finalMessage, finalKey = decrypt(key, ciphertext)
        deciphered_key = ""
        # print(finalMessage)
        # print(finalKey)
        for letter in "abcdefghijklmnopqrstuvwxyz":
            if letter not in finalKey.values():
                deciphered_key += letter
                continue
            else:
                for key, value in finalKey.items():
                    if(value == letter):
                        deciphered_key += key
                        break

        deciphered_text = finalMessage


        print("Ciphertext: " + ciphertext) # Do not change this
        print("Deciphered Plaintext: " + deciphered_text) # Do not change this
        print("Deciphered Key: " + deciphered_key) # Do not change this

        return deciphered_text, deciphered_key # Do not change this

if __name__ == '__main__': # Do not change this
    DecipherText() # Do not change this

