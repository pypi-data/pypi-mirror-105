from typing import List, Type

from .baserule import BaseRule
from . import Rule


class SubstringFields(BaseRule):
    subwords: List[str]


class SubstringRule(Rule):
    """Правило"""

    fields: Type[BaseRule] = SubstringFields

    def on(self):
        return self.subwords is not None and any([word in self.domain.name
                                                  for word in self.subwords])
