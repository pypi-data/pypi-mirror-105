"""
6.GreenDomain  удаляет все записи с субдоменами от указаного в парметрах
домена второго уровня. тоесть Greendomain amazon.com удалит server2.amazon.com
 и любые другие субдомены из списка до начала проверки на синтаксис.
"""
from .baserule import BaseRule
from . import Rule


class RedDomainFields(BaseRule):
    domain_name: str


class RedDomainRule(Rule):
    fields = RedDomainFields

    def on(self):
        return self.domain.name.endswith(self.domain_name)
