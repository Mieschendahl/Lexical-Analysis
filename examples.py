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
specials = "+-*/%=!<>.,;:(){}[]\"\'\\"
total = lowers + uppers + digits + spaces + specials


def arithmetics(algo): 
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
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def calculator(algo): 
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
        "x := 0", True,
        "x := 0; y:=x+1;", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5;", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos; a := 1/(xpos + ypos);", True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def json(algo): 
    alpha = digits + lowers + spaces + specials
    stringcontent = altstr(alpha.replace("\"", ""))
    w = altstr(" \n\t")
    regexes = [
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\""))),  # string
        Sym(":"),  # seperator
        Sym(","),  # next pair
        altstr("{["),  # left brackets
        altstr("}]"),  # right brackets
        repp(w),  # white spaces
    ]
    problems = [
"""
{
    "birthday" : "13.1.200"
}
""",
True,
"""
{
    "shoppinglist" : [
        "today" : "fish",
        "tommorrow" : ["rice", "garlic"]
    ],
}
""",
True,
"""
{
    "hello" : "test",
    "text": {
        "another" : "test",
        "and" : ["so", "on"]
    },
    "the next": "text",
    "final" : {
        "recursion" : {
            "recursion" : {
                "recursion" : ["hi", "this \\\" should \\\" work!"]
            }
        }
    }
}
""",
True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def xml(algo): 
    alpha = digits + lowers + spaces + specials
    stringcontent = altstr(alpha.replace("\"", ""))
    xmlcontent = altstr(alpha.replace("<", "").replace(">", ""))
    w = altstr(" \n\t")
    a = altstr(lowers + uppers)
    d = altstr(digits)
    string = con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    regexes = [
        con(constr("<"), con(rep(w), con(repp(a), con(rep(w), con(rep(con(repp(w), con(repp(a), con(Sym("="), string)))), Sym(">")))))),  # opening tags
        con(constr("</"), con(rep(w), con(repp(a), con(rep(w), Sym(">"))))),  # closing tags
        repp(w),  # white spaces
        xmlcontent  # content
    ]
    problems = [
"""
<day></day>
""",
True,
"""
< day ></ day >
""",
True,
"""
<day x="test"></ day >
""",
True,
"""
<day x="test" y="test"></ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests"></ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">abc</ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">
    <recursion level="1">
        <recursion level="2">
            <hi>this work to!</hi>
        </recursion>
    </recursion>
</ day >
""",
True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("<"), constr("</")), con(rep(w), repp(a))),  # left bracket
        Sym(">"),  # right bracket
        Sym("="),
        repp(w),  # white spaces
        string,  # strings
        xmlcontent  # content
    ]
    problems = [
"""
<day></day>
""",
True,
"""
< day ></ day >
""",
True,
"""
<day x="test"></ day >
""",
True,
"""
<day x="test" y="test"></ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests"></ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">abc</ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">
    <recursion level="1">
        <recursion level="2">
            <hi>this work to!</hi>
        </recursion>
    </recursion>
</ day >
""",
True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def python(algo): 
    alpha = digits + lowers + spaces + specials
    d = altstr(digits)
    nz = altstr(nonzero)
    a = altstr(lowers + uppers)
    w = altstr(" \t")
    
    regexes = [
        constr("if"),  # keyword
        constr("else"),  # keyword
        constr("def"),  # keyword
        constr("return"),  # keyword
        constr("print"),  # keyword
        Sym("\n"),  # new line
        Sym(":"),  # new block
        Sym(","),  # new argument
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        altstr("(["),  # left brackets
        altstr(")]"),  # right brackets
        altstr("+-*/"),  # operators
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # 12
        alt(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
    ]
    problems = [
"""
a = 10
""",
True,
"""
a = 10
b = (20 + a)
""",
True,
"""
a = 10
b = 20
c -= a*a if a <= b else [0] * len(a)
""",
True,
"""
def hello():
    return res
""",
True,
"""
def prob(x):
    res = 0
    if x + 10 <= 5:
        res = 1
    return res
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)
""",
True,
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
            arithmetics(algo)
            calculator(algo)
            json(algo)
            xml(algo)
            python(algo)
        else:
            arithmetics(algo)
            calculator(algo)
            json(algo)
            xml(algo)
            python(algo)
        save_statistics(algo.value)
    print("Evaluation complete (use plot_statistics.py to plot the results)")
