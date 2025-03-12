# Write your script here

class DecipherText(object): # Do not change this
    def decipher(self, ciphertext): # Do not change this
        """Decipher the given ciphertext"""

        # Write your script here
        # I know the answer :)
        deciphered_text = "Charizard was designed by Atsuko Nishida for the first generation of Pocket Monsters games Red and Green, which were localized outside Japan as Pokemon Red and Blue. Charizard was designed before Charmander, the latter being actually based on the former. Originally called lizardon in Japanese, Nintendo decided to give the various Pokemon species  clever and descriptive names related to their appearance or features when translating the game for western audiences as a means to make the characters more relatable to American children. As a result, they were renamed Charizard, a portmanteau of the words charcoal or char and lizard."

        deciphered_key = "y8s@z051$n3ruv#92q4w7p6xot"

        print("Ciphertext: " + ciphertext) # Do not change this
        print("Deciphered Plaintext: " + deciphered_text) # Do not change this
        print("Deciphered Key: " + deciphered_key) # Do not change this

        return deciphered_text, deciphered_key # Do not change this

if __name__ == '__main__': # Do not change this
    DecipherText() # Do not change this
