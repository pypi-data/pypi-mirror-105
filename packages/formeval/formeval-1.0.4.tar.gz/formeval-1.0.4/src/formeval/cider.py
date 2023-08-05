import collections
import math
from .evaluator import FormEvaluator
from .processor import RegexProcessor
from .utils import UnknownCandidatesError, combine_scores_candidates_references


def ngram_counts(tokens, n):
    if n == 1:
        return collections.Counter(tokens)
    return collections.Counter(' '.join(tokens[i: i + n]) for i in range(len(tokens) - n + 1)) \
        if len(tokens) >= n else {}


def get_ngram_counts(data, n):
    res = [collections.defaultdict(list) for _ in range(n)]
    for key, values in data.items():
        for tokens in values:
            for i in range(1, n):
                count = ngram_counts(tokens, i)
                res[i][key].append(count)
    return res


def get_idf(ngram_count):
    n = len(ngram_count)
    num_documents = len(ngram_count[1])
    ngram_in_documents = [[] for _ in range(n)]
    for i in range(1, n):
        for key, counters in ngram_count[i].items():
            ngram_in_documents[i].extend(list(set(key for counter in counters for key in counter.keys())))
    ngram_in_documents = [collections.Counter(vec) for vec in ngram_in_documents]
    return {k: math.log(num_documents / count) for i in range(n) for k, count in ngram_in_documents[i].items()}


def get_tf(ngram_count):
    n = len(ngram_count)
    res = [collections.defaultdict(list) for _ in range(n)]
    for i in range(1, n):
        for key, counters in ngram_count[i].items():
            for counter in counters:
                denominator = sum(counter.values())
                res[i][key].append({ngram: counter / denominator for ngram, counter in counter.items()})
    return res


def tfidf(tf, idf):
    n = len(tf)
    res = [collections.defaultdict(list) for _ in range(n)]
    for i in range(1, n):
        for key, tfs_list in tf[i].items():
            for tfs in tfs_list:
                length = sum(tfs.values())
                tf_idf = {ngram: _tf * idf.get(ngram, 0) for ngram, _tf in tfs.items()}
                norm = math.sqrt(sum(v * v for v in tf_idf.values()))
                res[i][key].append((tf_idf, norm, length))
    return res


def sparse_cosine_similarity(a, b, d_variant=True, sigma=6.0):
    a_vec, a_norm, a_length = a
    b_vec, b_norm, b_length = b
    norm = a_norm * b_norm
    if norm > 0:
        if d_variant:
            return math.e ** (-(float(a_length - b_length) ** 2) / (2 * sigma ** 2)) * sum(
                min(weight, b_vec.get(ngram, 0)) * b_vec.get(ngram, 0) for ngram, weight in a_vec.items()) / norm
        else:
            return sum(weight * b_vec.get(ngram, 0) for ngram, weight in a_vec.items()) / norm
    return 0


def _average(vec):
    return sum(vec) / len(vec)


class CiderEvaluator(FormEvaluator):
    def __init__(self, references, processor=None, already_processed=False, n=4, silent=True, d_variant=True):
        super(CiderEvaluator, self).__init__(silent=silent,
                                             processor=processor if processor else RegexProcessor(),
                                             already_processed=already_processed
                                             )
        self.log_build_references_started(references)
        self.n = n + 1
        self.d_variant = d_variant
        self.tokenized_references, self.references_ngram_count, self.references_tf = self.sentences_to_tf(
            references, self.n)
        self.idf = get_idf(self.references_ngram_count)
        self.references_tfidf = tfidf(self.references_tf, self.idf)
        self.log_build_references_completed()

    def sentences_to_tf(self, data, n):
        processed_data = self._process(data)
        ngram_count = get_ngram_counts(processed_data, n)
        tf = get_tf(ngram_count)
        return processed_data, ngram_count, tf

    def evaluate(self, candidates):
        self.log_evaluation_started(candidates)
        if not set(candidates.keys()).issubset(set(self.tokenized_references.keys())):
            raise UnknownCandidatesError

        tokenized_candidates, _, candidates_tf = self.sentences_to_tf(candidates, self.n)
        candidates_tfidf = tfidf(candidates_tf, self.idf)

        scores = {key: [0 for _ in range(len(_candidates))] for key, _candidates in candidates.items()}
        for i in range(1, self.n):
            for key, candidates in candidates_tfidf[i].items():
                for idx, candidate_tfidf in enumerate(candidates):
                    scores[key][idx] += _average([sparse_cosine_similarity(candidate_tfidf,
                                                                           reference_tfidf,
                                                                           self.d_variant)
                                                  for reference_tfidf in self.references_tfidf[i][key]])

        scores = {key: [score / (self.n - 1) for score in scores] for key, scores in scores.items()}
        avg_scores = _average([score for _scores in scores.values() for score in _scores])
        self.log_evaluation_completed()
        return avg_scores * 10, scores
