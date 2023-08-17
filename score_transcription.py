import argparse
import glob
import itertools
import json
import logging
import re
from pathlib import Path

import jiwer  # package for computing WER

logging.basicConfig(level=logging.INFO, filename="score_listenhome.log")


class MySubstituteWords(jiwer.AbstractTransform):
    """Replacement for jiwer's substitute transform that is much faster"""

    def __init__(self, substitutions):
        self.substitutions = substitutions

    def process_string(self, s):
        print('s is -------------')
        print(s)

        for word in s.split():
            if word not in self.substitutions:
                logging.info(f"OOV word: {word}")

        return " ".join(
            [
                self.substitutions[word] if (word in self.substitutions) else word
                for word in s.split()
            ]
        )

    def process_list(self, inp):
        return [self.process_string(s) for s in inp]
    

class ReduceToListOfWords(jiwer.AbstractTransform):
    """
    Transforms a single input sentence, or a list of input sentences, into
    a list of list of words, which is the expected format for calculating the
    edit operations between two input sentences.

    A sentence is assumed to be a string, where words are delimited by a token
    (such as ` `, space). Each string is expected to contain only a single sentence.
    Empty strings (no output) are removed for the list
    """

    def __init__(self, word_delimiter: str = " "):
        """
        :param word_delimiter: the character which delimits words. Default is ` ` (space).
        """
        self.word_delimiter = word_delimiter

    def process_string(self, s: str):
        return [w for w in s.split(self.word_delimiter) if len(w) >= 1]

    def process_list(self, inp):
        sentence_collection = []

        for sentence in inp:
            list_of_words = self.process_string(sentence)[0]

            sentence_collection.append(list_of_words)

        if len(sentence_collection) == 0:
            return []

        return sentence_collection


class MyRemovePunctuation(jiwer.AbstractTransform):
    """Replacement for jiwer's remove punctuation that allows more control."""

    def __init__(self, symbols):
        self.substitutions = f"[{symbols}]"

    def process_string(self, s):
        return re.sub(self.substitutions, "", s)

    def process_list(self, inp):
        return [self.process_string(s) for s in inp]


class PronDictionary:
    """Class to hold the pronunciation dictionary"""

    def __init__(self, filename):
        self.pron_dict = {}
        self.add_dict(filename)

    def add_dict(self, filename):
        with open(filename, "r", encoding="utf8") as f:
            lines = [line.strip() for line in f.readlines() if line[0] != "#"]
        pairs = [re.split("\t+", line) for line in lines]
        new_dict = {pair[0].strip(): pair[1] for pair in pairs if len(pair) == 2}
        self.pron_dict.update(new_dict)

    def lookup(self, word, sep=None):
        word_upper = word.upper()
        try:
            pron = self.pron_dict[word.upper()]
        except KeyError:
            logging.info(f"OOV word: {word_upper}")
            pron = word_upper
        if sep:
            pron = re.sub(" ", sep, pron)
        return pron


class Contractions:
    """Class to handle alternative spellings for contractions, e.g. don't vs do not"""

    def __init__(self, contraction_file):
        with open(contraction_file, "r") as f:
            contractions = [line.strip().split(", ") for line in f.readlines()]
        
        self.contract_dict = {v: k for k, v in contractions} | {
            k: v for k, v in contractions
        }

        self.contra_re = re.compile(
            "(" + "|".join(["\\b" + k + "\\b" for k in self.contract_dict.keys()]) + ")"
        )

    def make_sentence_forms(self, sentence):
        parts = re.split(self.contra_re, sentence.lower())
        # Filter out empty strings
        parts = [p for p in parts if p != ""]
        # ["I have"] -> ["I have", "I've"] etc
        parts = [
            [p, self.contract_dict[p]] if (p in self.contract_dict) else [p]
            for p in parts
        ]
        # Make all possible sentences with contracted and uncontracted word forms
        sentence_forms = ["".join(s) for s in itertools.product(*parts)]
        return sentence_forms


class SentenceScorer:
    def __init__(self, pron_dict=None, contractions=None):
        self.transformation = jiwer.Compose(
            [
                jiwer.RemoveKaldiNonWords(),
                jiwer.Strip(),
                MyRemovePunctuation("!*#,?"),
                jiwer.ToUpperCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.RemoveWhiteSpace(replace_by_space=True),
                # jiwer.SentencesToListOfWords(word_delimiter=" ")
                jiwer.ReduceToListOfListOfWords(word_delimiter=" "),
            ]
        )
        self.phoneme_transformation = None
        if pron_dict is not None:
            self.transformation = jiwer.Compose(
                [jiwer.RemoveKaldiNonWords(),
                jiwer.Strip(),
                MyRemovePunctuation("!*#,?"),
                jiwer.ToUpperCase(),
                jiwer.RemoveMultipleSpaces(),
                jiwer.RemoveWhiteSpace(replace_by_space=True),
                # jiwer.SentencesToListOfWords(word_delimiter=" ")
                jiwer.ReduceToListOfListOfWords(word_delimiter=" "),
                # MySubstituteWords(pron_dict.pron_dict)
                ]
            )
            self.phoneme_transformation = jiwer.Compose(
                [self.transformation]
            )

        self.contractions = contractions

    def get_word_sequence(self, sentence):
        return self.transformation(sentence)

    def get_phoneme_sequence(self, sentence):
        return (
            self.phoneme_transformation(sentence)
            if self.phoneme_transformation
            else None
        )

    def score(self, ref, hyp):
        if self.contractions:
            sentence_forms = self.contractions.make_sentence_forms(hyp)
        else:
            sentence_forms = [hyp]

        # print(type(sentence_forms))
        # print(self.transformation)
        # print(type(ref))
        # print(sentence_forms)


        measures = [
            jiwer.compute_measures(
                ref,
                m,
                truth_transform=self.transformation,
                hypothesis_transform=self.transformation,
            )
            for m in sentence_forms
        ]
        # print(measures)

        hits = [m["hits"] for m in measures]
        best_index = hits.index(max(hits))
        # print('ref is ---------------')
        # print(self.transformation(ref)[0])
        return (
            len(self.transformation(ref)[0]),  # n words in the reference
            measures[best_index]["hits"],  # n hits for best sentence form
            sentence_forms[best_index],  # Best form for the hypothesis
        )

    def score_phoneme(self, ref, hyp):
        if not self.phoneme_transformation:
            raise ValueError("No phoneme transformation defined")
        ref = self.phoneme_transformation(ref)
        hyp = self.phoneme_transformation(hyp)
        phoneme_measures = jiwer.compute_measures(
            ref,
            hyp,
        )
        return len(ref), phoneme_measures["hits"]


def score_listenhome(responses, scorer):

    responses = responses.copy()
    for r in responses:
        r["n_words"], r["hits_words"], sentence_form = scorer.score(
            r["prompt"], r["transcript"]
        )
        r["scored_form"] = sentence_form
        r["n_phonemes"], r["hits_phonemes"] = scorer.score_phoneme(
            r["prompt"], sentence_form
        )
    return responses


def score(ref, hyp):
    """Main entry point"""

    contraction = Contractions("jiwer_score/contractions.csv")
    pron_dict = PronDictionary("jiwer_score/beep-1.0")
    pron_dict.add_dict("jiwer_score/oov_dict.txt")
    scorer = SentenceScorer(pron_dict, contraction)

    temp = scorer.score(ref, hyp)

    score = temp[1]/temp[0]

    return score
