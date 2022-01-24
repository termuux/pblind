import dyno
from dyno.extensions.determiner import Determiner
from dyno.extensions.composer import ext_obj
from dyno.extensions.marketplace.activation import Activation
from dyno.core.natural import CreateResponse
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class Compute:
    def __init__(self, verbose_interface, config ):
        self.vint = verbose_interface
        self.config = config
        self.create_response = CreateResponse()
        self.determiner = Determiner(
            weight=TfidfVectorizer,
            similarity =cosine_similarity,
            argms=self.config.ext_determiner.get('args'),
            sensitivity=self.config.ext_determiner.get('sensitivity')
        )

    def execute(self):
        stream = dyno.utils.speechtt.SpeechText().reco_input()
        ext = self.determiner.extract(stream)

        if ext:
            response = self.create_response.form_positive_response(stream)
            dyno.utils.textts.TexttsEngine().tts_response(response)

            extexe = {'stream': stream, 'ext':ext}
            self.exeext(extexe)
        else:
            response = self.create_response.form_negative_response(stream)
            dyno.utils.textts.TexttsEngine().tts_response(response)

            
    def exeext(self, ext):
        if ext:
            ext_func_name = ext.get('ext').get('func')
            print(ext_func_name)
            self.vint.info_output('Running extension {0}'.format(ext_func_name))
            try:
                Activation.eassistant()
                ext_func_name = ext.get('ext').get('func')
                ext_func = ext_obj[ext_func_name]
                ext_func(**ext)
            except Exception as e:
                self.vint.error_output("Execution of extension {0} failed. {1}"
                                                    .format(ext_func_name, e))


        