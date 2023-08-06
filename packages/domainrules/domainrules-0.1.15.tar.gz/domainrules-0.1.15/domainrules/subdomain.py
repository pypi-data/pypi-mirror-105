from typing import Type

from .baserule import BaseRule
from . import Rule


class SubDomainFields(BaseRule):
    min_qty: int


class SubdomainRule(Rule):
    fields: Type[BaseRule] = SubDomainFields

    def on(self):
        return self.domain.name.count(".") > self.min_qty
