import traceback
from dataclasses import dataclass
from typing import Optional, cast, Any
from enum import Enum
from generation import *
from lexing import *


class Algo(Enum):
    DFA = 0
    MDFA = 1
    longest = 2
    lookahead = 3
    viable = 4


@dataclass
class Config:
    algo: Algo
    alpha: str
    regexes: list[Re]
    problems: list[Union[str, list[Union[str, int]]]]
    lookaheads: Optional[list[Re]] = None


def evaluate(config: Config):
    lookup = make_lookup(config.alpha)
    if config.algo is Algo.DFA:
        lex: Any = generate_DFA(config.alpha, config.regexes)
    elif config.algo is Algo.MDFA:
        lex = generate_MDFA(config.alpha, config.regexes)
    elif config.algo is Algo.longest:
        lex = generate_longest(config.alpha, config.regexes)
    elif config.algo is Algo.lookahead:
        lookaheads = config.lookaheads
        if lookaheads is None:
            lookaheads = [Eps() for _ in config.regexes]
        lex = generate_lookahead(config.alpha, config.regexes, lookaheads)
    elif config.algo is Algo.viable:
        lex = generate_viable(config.alpha, config.regexes)
    for i in range(0, len(config.problems), 2):
        word = cast(str, config.problems[i])
        assertion = config.problems[i+1]
        try:
            if config.algo is Algo.DFA:
                result: Any = lex_DFA(lookup, lex, word)
            elif config.algo is Algo.MDFA:
                result = lex_MDFA(lookup, lex, word)
            elif config.algo is Algo.longest:
                result = lex_longest(lookup, lex, word)
            elif config.algo is Algo.lookahead:
                result = lex_lookahead(lookup, lex, word)
            elif config.algo is Algo.viable:
                result = lex_longest(lookup, lex, word)
        except Exception as e:
            print(f"Error for {config.algo}:")
            print()
            print("Regexes:")
            for j, regex in enumerate(config.regexes):
                print(f"{j}: {regex}")
            print()

            print("word:")
            print(f"\"{word}\"")
            raise e
            
        if assertion is not None:
            tokens = []
            for j in range(0, len(assertion), 2):
                tokens.append(Token(cast(str, assertion[j]), cast(int, assertion[j+1])))
            if result != tokens:
                print(f"Assertion Error for {config.algo}:")
                traceback.print_stack()
                print()

                print("Regexes:")
                for j, regex in enumerate(config.regexes):
                    print(f"{j}: {regex}")
                print()

                print("word:")
                print(f"\"{word}\"")
                print()

                print("Assertion:")
                for j in range(max(len(result), len(tokens))):
                    equality = "=="
                    if j >= len(result):
                        a: Any = "Missing"
                        equality = "!="
                    else:
                        a = [result[j].value, config.regexes[result[j].index]]
                    if j >= len(tokens):
                        b: Any = "Missing"
                        equality = "!="
                    else:
                        b = [tokens[j].value, config.regexes[tokens[j].index]]
                    equality = equality if a == b else "!="
                    print(f"{a} {equality} {b}")
                exit()
