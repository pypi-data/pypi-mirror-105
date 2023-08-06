import re
from typing import Type

from . import Rule
from .baserule import BaseRule


class RegexpFields(BaseRule):
    regexp: str


class RegexpRule(Rule):
    fields: Type[BaseRule] = RegexpFields

    def set_rules(self, **kwargs):
        super().set_rules(**kwargs)
        self.reg = re.compile(self.regexp)
        return self

    def on(self):
        return re.match(self.reg, self.domain.name)
