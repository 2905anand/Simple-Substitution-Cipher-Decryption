from submissions.decipher_text import DecipherText

solve = DecipherText()
ciphertextFile = "./source/submissions/ciphertexts/example_ciphertext.txt"
f = open(ciphertextFile, "r")
ciphertext = f.read()
f.close()

deciphered_text, deciphered_key = solve.decipher(ciphertext)
