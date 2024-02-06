# type: ignore
from typing import Union, Callable, Any
from generation import *
from lexing import *
from evaluator import *


alpharange = lambda a, b: "".join(map(chr, list(range(ord(a), ord(b) + 1))))
lowers = alpharange("a", "z")
uppers = alpharange("A", "Z")
digits = alpharange("0", "9")
nonzero = alpharange("1", "9")
spaces = " \n\t"
specials = "+-*/%=!<>.,;(){}[]\"\'"
total = lowers + uppers + digits + spaces + specials


def eval_arithmetics(algo): 
    alpha = digits + ".+-/*() "
    d = altstr(digits)
    nz = altstr(nonzero)
    regexes = [
        alt(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        altstr("+-/*"),  # operators
        Sym("("),  # left bracket
        Sym(")"),  # right bracket
        repp(Sym(" ")),  # white space
    ]
    problems = [
        "0", True,
        "0.0", True,
        "10.01", True,
        "1 + 1", True,
        "1 / (1 - 100) * 0.250", True,
        "(0 * 1000 / 1000 + 1 + 2 + 3) + 3.1415926536", True,
        "0..0", False,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def eval_calculator(algo): 
    alpha = digits + lowers + ".+-/*() \n\t;=:"
    d = altstr(digits)
    nz = altstr(nonzero)
    ops = altstr("+-/*")
    a = altstr(lowers + uppers)
    w = altstr(" \n\t")
    regexes = [
        alt(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        ops,  # operators
        Sym("("),  # left bracket
        Sym(")"),  # right bracket
        repp(Sym(" ")),  # white space
        con(Sym(":"), Sym("=")),  # assignment operator
        Sym(";"),  # instruction seperator
    ]
    problems = [
        "x : 0", False,
        "x := 0", True,
        "x := 0; y:=x+1;", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5;", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos; a := 1/(xpos + ypos);", True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


    
# in increasing order


if __name__ == "__main__":
    print("Starting evaluation (this might take a while)")
    algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
    for algo in algos:
        print(f"Evaluating {algo.value}")
        clear_statistics()
        if algo is Algo.lookahead:
            pass
        elif algo is Algo.viable:
            eval_arithmetics(algo)
            eval_calculator(algo)
        else:
            eval_arithmetics(algo)
            eval_calculator(algo)
        save_statistics(algo.value)
    print("Evaluation complete (use plot_statistics.py to plot the results)")
