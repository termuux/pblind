from . import composer
from dyno.tools.symaps import symbol_maps


class Determiner:
    def __init__(self, weight, similarity , argms, sensitivity):
        self.weight = weight
        self.similarity = similarity
        self.argms = argms
        self.vectorize = self.create_vectorizer()
        self.dsensitivity = sensitivity

    @property
    def exts(self):
        return composer.control_exts + composer.basic_exts

    @property
    def tags(self):
        tags_list = []
        for ext in self.exts:
            tags_list.append(ext['tags'].split(','))
        return [','.join(tag) for tag in tags_list]

    def extract(self, text):
        train = self.train_model()
        wtext = self.sym_to_words(text)

        test = self.vectorize.transform([wtext])

        simities = self.similarity(train, test) 
        eindex = simities.argsort(axis=None)[-1]  
        if simities[eindex] > self.dsensitivity:
            ekey = []
            for ext in enumerate(self.exts):
                if ext[0] == eindex:
                    ekey.append(ext)
            return ekey[0][1]
        else:
            return None

    def sym_to_words(self, symtext):
        wtext = ''
        for word in symtext.split():
            if word in symbol_maps.values():
                for index, entry in symbol_maps.items():
                    if entry == word:
                        wtext += ' ' + index
            else:
                wtext += ' ' + word
        return wtext

    def create_vectorizer(self):
        return self.weight(**self.argms)

    def train_model(self):
        return self.vectorize.fit_transform(self.tags)

