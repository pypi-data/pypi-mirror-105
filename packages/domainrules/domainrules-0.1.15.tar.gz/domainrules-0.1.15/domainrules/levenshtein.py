from typing import Type

from Levenshtein._levenshtein import distance
from pydantic import validator

from .validators import gt0
from .baserule import BaseRule
from . import Rule


class LevenshteinFields(BaseRule):
    possible: int
    base_name: str
    _gt0_possible = validator("possible", allow_reuse=True)(gt0)


class LevenshteinRule(Rule):
    fields: Type[BaseRule] = LevenshteinFields

    def on(self):
        domain_name = self.domain.name.replace(".", "").replace("-", "")
        base_name = self.base_name.replace(".", "").replace("-", "")
        return distance(domain_name, base_name) < self.possible
