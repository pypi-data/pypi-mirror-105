import random

class Enigma:

    def __init__(self, seed):

        self.tokens = """1234567890-=!\"£$%^&*()_+{}~[]#:@;'<>?,./|\\qwertyuiopasdfghjklzxcvbnmmQWERTYUIOPASDFGHJKLZXCVBNM """
        self.characters = self.tokens

        self.tokens = [token for token in self.tokens]

        random.seed(seed)
        random.shuffle(self.tokens)

        self.dtokens = {}

        for index, token in enumerate([t for t in self.tokens]):

            self.dtokens[token] = self.characters[index]

        self.rdtokens = {self.dtokens[a]: a for a in self.dtokens}

    def decrypt(self, message):

        m = ''

        for char in message:

            if char in self.rdtokens:

                m += self.rdtokens[char]

        return m

    def encrypt(self, message):

        m = ''

        for char in message:

            if char in self.dtokens:

                m += self.dtokens[char]

        return m

    def encrypt_json(self, json):

        nj = {}

        for t in json:

            if type(t) == str:

                nj[self.encrypt(t)] = self.encrypt(json[t])

            else:

                nj[self.encrypt(t)] = json[t]

        return nj

    def decrypt_json(self, json):

        nj = {}

        for t in json:

            if type(t) == str:

                nj[self.decrypt(t)] = self.decrypt(json[t])

            else:

                nj[self.decrypt(t)] = json[t]

        return nj


def auth_generator(seg=4, cpseg=5, sep='..', characters='1234567890!£$%^&*abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'):

    token = []

    for s in range(seg):

        t = ''

        for c in range(cpseg):

            t += random.choice(characters)

        token.append(t)

    return sep.join(token)