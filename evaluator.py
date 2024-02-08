import os, errno
import traceback
from dataclasses import dataclass
from typing import Optional, cast, Any
from enum import Enum
from regex import *
from generation import *
from lexing import *
from time import time


class Algo(Enum):
    DFA = "DFA"
    MDFA = "MDFA"
    longest = "longest"
    lookahead = "lookahead"
    viable = "viable"

class Mode(Enum):
    exact = 0
    vague = 1


@dataclass
class Config:
    algo: Algo
    alpha: str
    regexes: list[Re]
    problems: list[Union[str, list[Union[str, int]]]]
    lookaheads: Optional[list[Re]] = None
    mode: Mode = Mode.exact


statistics = {
    "generation_size": [],
    "generation_time": [],
    "lexing_steps": [],
    "lexing_time": [],
}


def clear_statistics():
    statistics["generation_size"] = []
    statistics["generation_time"] = []
    statistics["lexing_steps"] = []
    statistics["lexing_time"] = []


def save_statistics(directory, filename):
    directory = "./statistics/" + directory + "/"
    try:
        os.makedirs(directory)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    with open(directory + filename + ".py", "w") as file:
        file.write(repr(statistics))

def load_statistics(directory, filename):
    directory = "./statistics/" + directory + "/"
    with open(directory + filename + ".py", "r") as file:
        return eval(file.read())
    


def evaluate(config: Config):
    lookup = make_lookup(config.alpha)
    regexes_size = sum(size(re) for re in config.regexes)
    lex_size = -1
    if config.algo is Algo.DFA:
        start = time()
        lex: Any = generate_DFA(config.alpha, config.regexes)
        end = time()
        lex_size = sum(len(l.delta) for l in lex)
    elif config.algo is Algo.MDFA:
        start = time()
        lex = generate_MDFA(config.alpha, config.regexes)
        end = time()
        lex_size = len(lex.delta)
    elif config.algo is Algo.longest:
        start = time()
        lex = generate_longest(config.alpha, config.regexes)
        end = time()
        lex_size = len(lex[0].delta) + len(lex[2].delta)
    elif config.algo is Algo.lookahead:
        lookaheads = config.lookaheads
        if lookaheads is None:
            lookaheads = [All for _ in config.regexes]
        if len(lookaheads) != len(config.regexes):
            raise Exception("Regexes and lookaheads do not pair up!")
        regexes_size += sum(size(re) for re in lookaheads)
        start = time()
        lex = generate_lookahead(config.alpha, config.regexes, lookaheads)
        end = time()
        lex_size = sum(map(lambda l: len(l.delta), lex[0])) + len(lex[3].delta)
    elif config.algo is Algo.viable:
        start = time()
        lex = generate_viable(config.alpha, config.regexes)
        end = time()
        lex_size = len(lex[0].delta) + len(lex[2].delta)
    statistics["generation_size"].append((regexes_size, lex_size))
    statistics["generation_time"].append((regexes_size, end - start))

    for i in range(0, len(config.problems), 2):
        word = cast(str, config.problems[i])

        try:
            clear_lexing_statistics()

            if config.algo is Algo.DFA:
                start = time()
                result: Any = lex_DFA(lookup, lex, word)
                end = time()
            elif config.algo is Algo.MDFA:
                start = time()
                result = lex_MDFA(lookup, lex, word)
                end = time()
            elif config.algo is Algo.longest:
                start = time()
                result = lex_longest(lookup, lex, word)
                end = time()
            elif config.algo is Algo.lookahead:
                start = time()
                result = lex_lookahead(lookup, lex, word)
                end = time()
            elif config.algo is Algo.viable:
                start = time()
                result = lex_longest(lookup, lex, word)
                end = time()

            statistics["lexing_steps"].append((len(word), lexing_statistics["transitions"]))
            statistics["lexing_time"].append((len(word), end - start))
        
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
            
        assertion = config.problems[i+1]
        if config.mode is Mode.exact:
            tokens = []
            for j in range(0, len(assertion), 2):
                tokens.append(Token(cast(str, assertion[j]), cast(int, assertion[j+1])))
            if result != tokens:
                print(f"Assertion Error for {config.algo}:")
                traceback.print_stack()
                print()

                print("word:")
                print(f"\"{word}\"")
                print()

                print("Assertion: (lexer left vs user right)")
                for j in range(max(len(result), len(tokens))):
                    equality = "=="
                    if j >= len(result):
                        a: Any = "Missing"
                        equality = "!="
                    else:
                        a = [result[j].value, result[j].index]
                    if j >= len(tokens):
                        b: Any = "Missing"
                        equality = "!="
                    else:
                        b = [tokens[j].value, tokens[j].index]
                    equality = equality if a == b else "!="
                    print(f"{a} {equality} {b} ")
                exit()
        elif config.mode is Mode.vague:
            if (result == [] and assertion) or (result != [] and not assertion):
                print(f"Assertion Error for {config.algo}:")
                traceback.print_stack()
                print()

                print("word:")
                print(f"\"{word}\"")
                print()

                print("Assertion:")
                if result != []:
                    print("Lexer found valid tokenization, i.e.")
                    for j in range(len(result)):
                        a = [result[j].value, result[j].index]
                        print(f"{a}")
                else:
                    print("Lexer did not find valid tokenization!")
                print("But valid tokenization should exists!" if assertion else "But valid tokenization should not exists!")
                exit()
