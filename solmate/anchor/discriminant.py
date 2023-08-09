from podite import (Variant)

from .sighash import sighash
from ..utils import snake_to_pascal


class AccountDiscriminant(Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("account", snake_to_pascal(self.name.lower()))


class InstructionDiscriminant(Variant):
    def assign_value(self, cls, prev_value):
        self.value = sighash("global", self.name.lower())
