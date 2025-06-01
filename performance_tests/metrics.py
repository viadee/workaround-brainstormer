from dataclasses import dataclass
from typing import Optional

@dataclass
class LLMJudgeDomainRelevanceMetric():
    assessment: Optional[bool] = None
    assessment_explaination: Optional[str] = None
    

@dataclass
class MetricResults:
    llm_judge_domain_relevance: LLMJudgeDomainRelevanceMetric
    bert_score: Optional[int]= None
    self_bleu: Optional[int]= None
    distinct: Optional[int]= None
    perplexity: Optional[int]= None
    

@dataclass
class ProcessWorkaroundsMetricResults:
    avg_bert_score: int
    llm_judge_domain_relevance_quality: float

    