import re
import nltk

class NaturalProcess:
    def __init__(self):
        pass

    @staticmethod
    def is_response_positive(response):
        return response in ['yup', 'yes', 'y', 'true', 'sure', 'ok']

    @staticmethod
    def is_response_negative(response):
        return response in ['no', 'not', 'never', 'cant', 'dont' ]
    
    @staticmethod
    def create_speech_parts(text):
        return nltk.pos_tag(nltk.word_tokenize(text))
    
    @staticmethod
    def has_query_modal(speech_parts):
        pgrammar = 'QS: {<MD><PRP><VB>}'
        corpus = nltk.RegexpParser(pgrammar)
        output = corpus.parse(speech_parts)
        for subtree in output.subtrees():
            if subtree.label() in ['QS', 'MD', 'WD']:
                return True

    @staticmethod
    def has_query_inversion(speech_parts):
        pgrammar = 'QS: {<VBP><PRP>}'
        corpus = nltk.RegexpParser(pgrammar)
        output = corpus.parse(speech_parts)
        for subtree in output.subtrees():
            if subtree.label() in ['QS']:
                return True


    @staticmethod
    def extract_verb(speech_parts):
        for part in speech_parts:
            if part[1] in ['VB']:
                return part[0]
        return ' '

    @staticmethod
    def extract_modal(speech_parts):
        for part in speech_parts:
            if part[1] in ['MD']:
                return part[0]
        return ' '

    @staticmethod
    def extract_noun(speech_parts):
        for part in speech_parts:
            if part[1] in ['NN', 'NNS', 'NNP', 'NNPS']:
                return part[0]
        return ' '


class CreateResponse(NaturalProcess):
    
    def __init__(self):
        super().__init__()

    def form_positive_response(self, sentence):
        presponse = self.form_response(sentence)
        if presponse:
            return 'Yes, ' + presponse

    def form_negative_response(self, sentence):
        neresponse = self.form_response(sentence)
        if neresponse:
            return 'No, ' + nresponse

    def form_response(self, sentence):
        speech_parts = self.create_speech_parts(sentence)
        verb = self.extract_verb(speech_parts)
        modal = self.extract_modal(speech_parts)
        noun = self.extract_noun(speech_parts)

        if self.has_query_modal(speech_parts):
            answer = 'I ' + modal + ' ' + verb + ' ' + noun
        elif self.has_query_inversion(speech_parts):
            answer = 'I ' + ' ' + verb + ' ' + noun
        else:
            answer = ''

        return re.sub('\s\s+', ' ', answer)

