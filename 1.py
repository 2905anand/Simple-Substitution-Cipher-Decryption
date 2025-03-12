# Simple Substitution Cipher Hacker
  2. # https://www.nostarch.com/crackingcodes/ (BSD Licensed)
  3.
  4. import os, re, copy, pyperclip, simpleSubCipher, wordPatterns,
       makeWordPatterns
  5.
  6.
  7.
  8.
  9.
 10. LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
 11. nonLettersOrSpacePattern = re.compile('[^A-Z\s]')
 12.
 13. def main():
 14.     message = 'Sy l nlx sr pyyacao l ylwj eiswi upar lulsxrj isr
           sxrjsxwjr, ia esmm rwctjsxsza sj wmpramh, lxo txmarr jia aqsoaxwa
           sr pqaceiamnsxu, ia esmm caytra jp famsaqa sj. Sy, px jia pjiac
           ilxo, ia sr pyyacao rpnajisxu eiswi lyypcor l calrpx ypc lwjsxu sx
           lwwpcolxwa jp isr sxrjsxwjr, ia esmm lwwabj sj aqax px jia
           rmsuijarj aqsoaxwa. Jia pcsusx py nhjir sr agbmlsxao sx jisr elh.
           -Facjclxo Ctrramm'
 15.
 16.     # Determine the possible valid ciphertext translations:
 17.     print('Hacking...')
 18.     letterMapping = hackSimpleSub(message)
 19.
 20.     # Display the results to the user:
 21.     print('Mapping:')
 22.     print(letterMapping)
 23.     print()
 24.     print('Original ciphertext:')
 25.     print(message)
 26.     print()
 27.     print('Copying hacked message to clipboard:')
 28.     hackedMessage = decryptWithCipherletterMapping(message, letterMapping)
 29.     pyperclip.copy(hackedMessage)
 30.     print(hackedMessage)
 31.
 32.
 33. def getBlankCipherletterMapping():
 34.     # Returns a dictionary value that is a blank cipherletter mapping:
 35.     return {'A': [], 'B': [], 'C': [], 'D': [], 'E': [], 'F': [], 'G': [],
           'H': [], 'I': [], 'J': [], 'K': [], 'L': [], 'M': [], 'N': [],
           'O': [], 'P': [], 'Q': [], 'R': [], 'S': [], 'T': [], 'U': [],
           'V': [], 'W': [], 'X': [], 'Y': [], 'Z': []}
 36.
 37.
 38. def addLettersToMapping(letterMapping, cipherword, candidate):
 39.     # The letterMapping parameter takes a dictionary value that
 40.     # stores a cipherletter mapping, which is copied by the function.
 41.     # The cipherword parameter is a string value of the ciphertext word.
 42.     # The candidate parameter is a possible English word that the
 43.     # cipherword could decrypt to.
 44.
 45.     # This function adds the letters in the candidate as potential
 46.     # decryption letters for the cipherletters in the cipherletter
 47.     # mapping.
 48.
 49.
 50.     for i in range(len(cipherword)):
 51.         if candidate[i] not in letterMapping[cipherword[i]]:
 52.             letterMapping[cipherword[i]].append(candidate[i])
 53.
 54.
 55.
 56. def intersectMappings(mapA, mapB):
 57.     # To intersect two maps, create a blank map and then add only the
 58.     # potential decryption letters if they exist in BOTH maps:
 59.     intersectedMapping = getBlankCipherletterMapping()
 60.     for letter in LETTERS:
 61.
 62.         # An empty list means "any letter is possible". In this case just
 63.         # copy the other map entirely:
 64.         if mapA[letter] == []:
 65.             intersectedMapping[letter] = copy.deepcopy(mapB[letter])
 66.         elif mapB[letter] == []:
 67.             intersectedMapping[letter] = copy.deepcopy(mapA[letter])
 68.         else:
 69.             # If a letter in mapA[letter] exists in mapB[letter],
 70.             # add that letter to intersectedMapping[letter]:
 71.             for mappedLetter in mapA[letter]:
 72.                 if mappedLetter in mapB[letter]:
 73.                     intersectedMapping[letter].append(mappedLetter)
 74.
 75.     return intersectedMapping
 76.
 77.
 78. def removeSolvedLettersFromMapping(letterMapping):
 79.     # Cipherletters in the mapping that map to only one letter are
 80.     # "solved" and can be removed from the other letters.
 81.     # For example, if 'A' maps to potential letters ['M', 'N'], and 'B'
 82.     # maps to ['N'], then we know that 'B' must map to 'N', so we can
 83.     # remove 'N' from the list of what 'A' could map to. So 'A' then maps
 84.     # to ['M']. Note that now that 'A' maps to only one letter, we can
 85.     # remove 'M' from the list of letters for every other letter.
 86.     # (This is why there is a loop that keeps reducing the map.)
 87.
 88.     loopAgain = True
 89.     while loopAgain:
 90.         # First assume that we will not loop again:
 91.         loopAgain = False
 92.
 93.         # solvedLetters will be a list of uppercase letters that have one
 94.         # and only one possible mapping in letterMapping:
 95.         solvedLetters = []
 96.         for cipherletter in LETTERS:
 97.             if len(letterMapping[cipherletter]) == 1:
 98.                 solvedLetters.append(letterMapping[cipherletter][0])
 99.
100.         # If a letter is solved, then it cannot possibly be a potential
101.         # decryption letter for a different ciphertext letter, so we
102.         # should remove it from those other lists:
103.         for cipherletter in LETTERS:
104.             for s in solvedLetters:
105.                 if len(letterMapping[cipherletter]) != 1 and s in
                       letterMapping[cipherletter]:
106.                     letterMapping[cipherletter].remove(s)
107.                     if len(letterMapping[cipherletter]) == 1:
108.                         # A new letter is now solved, so loop again:
109.                         loopAgain = True
110.     return letterMapping
111.
112.
113. def hackSimpleSub(message):
114.     intersectedMap = getBlankCipherletterMapping()
115.     cipherwordList = nonLettersOrSpacePattern.sub('',
           message.upper()).split()
116.     for cipherword in cipherwordList:
117.         # Get a new cipherletter mapping for each ciphertext word:
118.         candidateMap = getBlankCipherletterMapping()
119.
120.         wordPattern = makeWordPatterns.getWordPattern(cipherword)
121.         if wordPattern not in wordPatterns.allPatterns:
122.             continue # This word was not in our dictionary, so continue.
123.
124.         # Add the letters of each candidate to the mapping:
125.         for candidate in wordPatterns.allPatterns[wordPattern]:
126.             addLettersToMapping(candidateMap, cipherword, candidate)
127.
128.         # Intersect the new mapping with the existing intersected mapping:
129.         intersectedMap = intersectMappings(intersectedMap, candidateMap)
130.
131.     # Remove any solved letters from the other lists:
132.     return removeSolvedLettersFromMapping(intersectedMap)
133.
134.
135. def decryptWithCipherletterMapping(ciphertext, letterMapping):
136.     # Return a string of the ciphertext decrypted with the letter mapping,
137.     # with any ambiguous decrypted letters replaced with an underscore.
138.
139.     # First create a simple sub key from the letterMapping mapping:
140.     key = ['x'] * len(LETTERS)
141.     for cipherletter in LETTERS:
142.         if len(letterMapping[cipherletter]) == 1:
143.             # If there's only one letter, add it to the key:
144.             keyIndex = LETTERS.find(letterMapping[cipherletter][0])
145.             key[keyIndex] = cipherletter
146.         else:
147.             ciphertext = ciphertext.replace(cipherletter.lower(), '_')
148.             ciphertext = ciphertext.replace(cipherletter.upper(), '_')
149.     key = ''.join(key)
150.
151.     # With the key we've created, decrypt the ciphertext:
152.     return simpleSubCipher.decryptMessage(key, ciphertext)
153.
154.
155. if __name__ == '__main__':
156.     main()