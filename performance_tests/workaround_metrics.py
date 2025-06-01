from dataclasses import dataclass


@dataclass
class MetricResults:
    bert_score: int
    self_bleu: int
    distinct: int
    perplexity: int