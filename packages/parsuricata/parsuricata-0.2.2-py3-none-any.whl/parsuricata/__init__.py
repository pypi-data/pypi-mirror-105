__version__ = "0.2.2"

from ._parser import parser
from .rules import *
from .transformer import RuleTransformer


def parse_rules(source: str) -> RulesList:
    tree = parser.parse(source)
    return RuleTransformer().transform(tree)
