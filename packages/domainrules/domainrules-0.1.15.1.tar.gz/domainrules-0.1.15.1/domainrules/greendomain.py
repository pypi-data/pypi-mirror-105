"""
6.GreenDomain  удаляет все записи с субдоменами от указаного в парметрах
домена второго уровня. тоесть Greendomain amazon.com удалит server2.amazon.com
 и любые другие субдомены из списка до начала проверки на синтаксис.
"""
from typing import Type

from pydantic import BaseModel

from .baserule import BaseRule
from . import Rule


class GreenDomainFields(BaseRule):
    domain_name: str


class GreenDomainRule(Rule):
    fields: Type[BaseModel] = GreenDomainFields

    def set_rules(self, **kwargs):
        super().set_rules(**kwargs)
        self.bal *= -1
        return self

    def on(self):
        return self.domain.name.endswith(self.domain_name)
