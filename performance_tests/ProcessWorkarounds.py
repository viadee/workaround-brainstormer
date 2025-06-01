from dataclasses import dataclass, asdict
from typing import List, Optional
from enum import Enum
from workaround_metrics import MetricResults


class PromptStrategys(Enum):
    SinglePrompt = "SinglePrompt"
    DivideThree = "DivideThree"

@dataclass
class WorkaroundAssesmentEntry:
    text: str
    test_results: Optional[MetricResults]

@dataclass
class ProcessWorkaroundsAssesmentEntry:
    id: int
    prompt_strategy: str
    process_description: str
    workarounds: List[WorkaroundAssesmentEntry]
    token_count: Optional[int]

    # Custom serialization method
    def to_dict(self):
        return asdict(self)

