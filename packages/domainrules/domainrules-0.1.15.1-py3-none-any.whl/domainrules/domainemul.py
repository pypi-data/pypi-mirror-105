"""
6.GreenDomain  удаляет все записи с субдоменами от указаного в парметрах
домена второго уровня. тоесть Greendomain amazon.com удалит server2.amazon.com
 и любые другие субдомены из списка до начала проверки на синтаксис.
"""
from typing import Type

from pydantic import BaseModel

from .baserule import BaseRule
from . import Rule


class DomainEmulFields(BaseRule):
    domain_part: str  # "com"


class DomainEmulRule(Rule):
    fields: Type[BaseModel] = DomainEmulFields

    def on(self):
        return any([p in self.domain.name
                    for p in [
                        f"-{self.domain_part}.",
                        f".{self.domain_part}.",
                        f"-{self.domain_part}-",
                    ]])
