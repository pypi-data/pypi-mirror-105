from random import randint as r
import re

class Compliment:

    def __init__ (self):

        self.templates_arr = [
            'I can tell ',
            'I must say ',
            '9 out of 10 docotrs say ',
            'I can\'t believe ',
            'I reckon ',
            'I think ',
            'I\'ve always thought ',
            'I\'ve heard ',
            'People say ',
            'They say ',
            'It\'s True ',
        ]

        self.tangible_singular_prop_arr = [
            "ass",
  "belly button",
  "booty",
  "bottom lip",
  "brain",
  "bum",
  "butt",
  "chin",
  "demeanour",
  "face",
  "fashion sense",
  "forehead",
  "heart",
  "index finger",
  "keister",
  "laugh",
  "left foot",
  "left hand",
  "little toe",
  "mind",
  "mouth",
  "neck",
  "outlook on life",
  "posterior",
  "radiance",
  "right foot",
  "right hand",
  "smile",
  "soul",
  "thumb",
  "tongue",
  "tush",
  "tushie",
  "vibe",
  "voice",
  "way of thinking",
  "work ethic",
            "nape"
        ]

        self.tangible_multiple_prop_arr = [
            "ankles",
  "buttocks",
  "calves",
  "clothes",
            "curves",
  "ears",
  "elbows",
  "eyebrows",
  "eyelashes",
  "eyes",
  "facial hair",
  "feet",
  "fingernails",
  "fingers",
  "forearms",
  "hair",
  "hands",
  "hips",
  "ideas",
            "jawline",
  "knees",
  "legs",
  "muscles",
  "skills",
  "skin",
  "strengths",
  "teeth",
  "thighs",
  "thoughts",
  "toenails",
  "toes",
  "wrists",
        ]

        self.adjectives_arr = [
            "adorable",
  "alluring",
  "amazeballs",
  "amazing",
  "angelic",
  "astonishing",
  "astounding",
  "attractive",
  "awe-inspiring",
  "awesome",
  "beautiful",
  "beguiling",
  "bewildering",
  "bewitching",
  "breathtaking",
  "charming",
  "comely",
  "crazy",
  "cute",
  "dazzling",
  "delightful",
  "divine",
  "dreamy",
  "exquisite",
  "extraordinary",
  "fantastic",
  "glamorous",
  "gorgeous",
  "great",
  "handsome",
  "heavenly",
  "hot",
  "impressive",
  "incredible",
  "insane",
  "irresistible",
  "lovely",
  "magnificent",
  "majestic",
  "marvellous",
  "marvelous",
  "mind-blowing",
  "mind-boggling",
  "nice",
  "perfect",
  "phenomenal",
  "pleasing",
  "preposterous",
  "pretty",
  "radiant",
  "ravishing",
  "remarkable",
  "sensational",
  "smashing",
  "spectacular",
  "splendid",
  "stunning",
  "stupefying",
  "stupendous",
  "sublime",
  "superb",
  "supercalifragilisticexpialidocious",
  "sweet",
  "tasty",
  "terrific",
  "tremendous",
  "unbelievable",
  "useful",
  "wonderful",
  "wowzers",
        ]

        self.adverb_arr = [
            "absolutely",
  "awfully",
  "bloody",
  "completely",
  "decidedly",
  "deeply",
  "devilishly",
  "distinctly",
  "entirely",
  "especially",
  "ever so",
  "exceedingly",
  "exceptionally",
  "extraordinarily",
  "extremely",
  "fairly",
  "frightfully",
  "highly",
  "hugely",
  "immensely",
  "incredibly",
  "inordinately",
  "insanely",
  "intensely",
  "mightily",
  "oh-so",
  "outstandingly",
  "particularly",
  "perfectly",
  "positively",
  "practically",
  "pretty",
  "purely",
  "quite",
  "radiantly",
  "rather",
  "really",
  "remarkably",
  "seriously",
  "simply",
  "so",
  "somewhat",
  "sort of",
  "supremely",
  "terribly",
  "thoroughly",
  "totally",
  "totes",
  "tremendously",
  "truly",
  "unusually",
  "utterly",
  "very",
  "virtually",
        ]



    def get_final_template(self):
        l = len(self.final_templates)-1
        return self.final_templates[r(0,l)]

    def get_adjective(self):

        l = len(self.adjectives_arr)-1
        return self.adjectives_arr[r(0,l)]

    def get_adverb(self):

        l= len(self.adverb_arr)-1
        return self.adverb_arr[r(0,l)]

    def get_descriptor(self):
        return ' '.join([self.get_adverb(), self.get_adjective()])

    def get_abstract_prop(self):

        l = len(self.abstract_prop_arr) - 1
        return self.abstract_prop_arr[r(0,l)]

    def get_tangible_singular_prop(self):

        l = len(self.tangible_singular_prop_arr) - 1
        return self.tangible_singular_prop_arr[r(0,l)]

    def get_tangible_multiple_prop(self):

        l = len(self.tangible_multiple_prop_arr) - 1
        return self.tangible_multiple_prop_arr[r(0,l)]

    def make_singular_form(self, text):
        if re.search('^[aeiou]', text):
            return 'an '+ text
        else :
            return 'a '+ text

    def get_template(self):
        l = len(self.template) -1
        return self.template[r(0,l)]

    def make_compliment(self) -> str:
        """Creates and returns a compliment."""

        self.abstract_prop_arr = [
            ' '.join([self.make_singular_form(self.get_descriptor()), self.get_tangible_singular_prop()]),

             ' '.join([self.get_descriptor(), self.
 get_tangible_multiple_prop()])
         ]

        self.final_templates = [
             'you are ' + self.get_descriptor(),
             'you have ' + self.get_abstract_prop()
        ]

        self.template = list(map(lambda x: x+ self.
 get_final_template(), self.templates_arr))

        return self.get_template()
