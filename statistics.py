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
specials = "_+-*/%=!<>.,;:(){}[]\"\'\\"
total = lowers + uppers + digits + spaces + specials


def arithmetics(algo): 
    alpha = digits + ".+-/*() "
    d = altstr(digits)
    nz = altstr(nonzero)
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
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
        "1 / (1 - 100)", True,
        "1 / (1 - 100)-1", True,
        "1 / (1 - 100) * 0.1", True,
        "1 / (1 - 100) * 0.250", True,
        "(0 * 1000 / 1000) + (3.14266)", True,
        "(0 * 1000 / 1000) + 3.1415926536", True,
        "(0 * 1000 / 1000 + 1 + 2 + 3) + 30", True,
        "(0 * 1000 / 1000 + 1 + 2 + 3) + 3.14159", True,
        "(0 * 1000 / 1000 + 1 + 2 + 3) + (3.1415926536 * (101))", True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    # statics for regex generation
    problems = []
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        altstr("+-/*"),  # operators
        Sym("("),  # left bracket
        Sym(")"),  # right bracket
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        altstr("+-/*"),  # operators
        Sym("("),  # left bracket
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        altstr("+-/*"),  # operators
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        alt(Sym("0"), con(nz, rep(d))),  # float number
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
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
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
        "x := 0; y:=x+1; z := (x*x);", True,
        "x := 0; y:=x+1; z := (x*x + y*y);", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5;", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := 1", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos; 0 + 0 := 1", True,
        "x := 0; y:=x+1; z := (x*x + y*y) * 0.5; xpos := -1; ypos:=xpos; a := 1/(xpos + ypos);", True,
    ]
    # statics for regex generation
    problems = []
    regexes = [
        con(a, rep(alt(a, d))),  # identifiers
        ops,  # operators
        Sym("("),  # left bracket
        Sym(")"),  # right bracket
        repp(Sym(" ")),  # white space
        con(Sym(":"), Sym("=")),  # assignment operator
        Sym(";"),  # instruction seperator
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(a, rep(alt(a, d))),  # identifiers
        ops,  # operators
        Sym("("),  # left bracket
        Sym(")"),  # right bracket
        repp(Sym(" ")),  # white space
        con(Sym(":"), Sym("=")),  # assignment operator
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        repp(Sym(" ")),  # white space
        con(Sym(":"), Sym("=")),  # assignment operator
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(a, rep(alt(a, d))),  # identifiers
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
}
""",
True,
"""
{
    "final" : {
    }
}
""",
True,
"""
{
    "final" : {
        "recursion" : {
        }
    }
}
""",
True,
"""
{
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
"""
{
    "hello" : "test",
    "text": {
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
    problems = []
    regexes = [
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\""))),  # string
        Sym(":"),  # seperator
        Sym(","),  # next pair
        repp(w),  # white spaces
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\""))),  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        rep(alt(stringcontent, constr("\\\""))),  # string
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
    test
</ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">
    <recursion level="1">
    </recursion>
</ day >
""",
True,
"""
<day x="test" y="test" z="the \\\" tests">
    <recursion level="1">
        <recursion level="2">
        </recursion>
    </recursion>
</ day >
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
    # statistics for regex expresssions
    problems = []
    regexes = [
        con(constr("<"), con(rep(w), con(repp(a), con(rep(w), con(rep(con(repp(w), con(repp(a), con(Sym("="), string)))), Sym(">")))))),  # opening tags
        con(constr("</"), con(rep(w), con(repp(a), con(rep(w), Sym(">"))))),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(rep(w), con(repp(a), con(rep(w), con(rep(con(repp(w), con(repp(a), con(Sym("="), string)))), Sym(">"))))),  # opening tags
        con(rep(w), con(repp(a), con(rep(w), Sym(">")))),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(repp(a), con(rep(w), con(rep(con(repp(w), con(repp(a), con(Sym("="), string)))), Sym(">")))),  # opening tags
        con(repp(a), con(rep(w), Sym(">"))),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(rep(w), con(rep(con(repp(w), con(repp(a), con(Sym("="), string)))), Sym(">"))),  # opening tags
        con(rep(w), Sym(">")),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        rep(con(repp(w), con(repp(a), con(Sym("="), string)))),  # opening tags
        con(rep(w), Sym(">")),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(repp(w), con(repp(a), con(Sym("="), string))),  # opening tags
        con(rep(w), Sym(">")),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(repp(a), con(Sym("="), string)),  # opening tags
        con(rep(w), Sym(">")),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(repp(a), string),  # opening tags
        con(rep(w), Sym(">")),  # closing tags
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))

    # different version of the lexing
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
    # statics for regex generation
    problems = []
    regexes = [
        con(alt(Sym("<"), constr("</")), con(rep(w), repp(a))),  # left bracket
        repp(w),  # white spaces
        string,  # strings
        xmlcontent  # content
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(alt(Sym("<"), constr("</")), con(rep(w), repp(a))),  # left bracket
        xmlcontent  # content
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        alt(Sym("<"), constr("</")),  # left bracket
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def python(algo): 
    alpha = digits + lowers + uppers + spaces + specials
    d = altstr(digits)
    nz = altstr(nonzero)
    a = altstr(lowers + uppers + "_")
    w = altstr(" \t")
    stringcontent = altstr(alpha.replace("\"", ""))
    
    regexes = [
        constr("if"),  # keyword
        constr("else"),  # keyword
        constr("def"),  # keyword
        constr("return"),  # keyword
        constr("print"),  # keyword
        constr("yield"),  # keyword
        Sym("\n"),  # new line
        Sym(":"),  # new block
        Sym(","),  # new argument
        Sym("."),  # attribute access
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        altstr("(["),  # left brackets
        altstr(")]"),  # right brackets
        altstr("+-*/"),  # operators
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
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
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)
""",
True,
"""
def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
"""
a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    # regex statistics
    problems = []
    regexes = [
        constr("if"),  # keyword
        constr("else"),  # keyword
        constr("def"),  # keyword
        constr("return"),  # keyword
        constr("print"),  # keyword
        constr("yield"),  # keyword
        Sym("\n"),  # new line
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        altstr("(["),  # left brackets
        altstr(")]"),  # right brackets
        altstr("+-*/"),  # operators
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        constr("return"),  # keyword
        constr("print"),  # keyword
        constr("yield"),  # keyword
        Sym("\n"),  # new line
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        altstr("(["),  # left brackets
        altstr(")]"),  # right brackets
        altstr("+-*/"),  # operators
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        altstr("(["),  # left brackets
        altstr(")]"),  # right brackets
        altstr("+-*/"),  # operators
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        repp(w),  # white spaces
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(a, rep(alt(a, d))),  # identifiers
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


    
def python_lookahead(algo):
    alpha = digits + lowers + uppers + spaces + specials
    d = altstr(digits)
    nz = altstr(nonzero)
    a = altstr(lowers + uppers + "_")
    w = altstr(" \t")
    stringcontent = altstr(alpha.replace("\"", ""))
    identifier = con(a, rep(alt(a, d)))  # identifiers
    regexes = [
        constr("if"),  # keyword 1
        constr("else"),  # keyword 2
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(a),  # 1
        negz(a),  # 2
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    problems = [
"""a""",
True,
"""
a
""",
True,
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
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)
""",
True,
"""
def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
"""
a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)
""",
True,
"""
def map(f, x):
    return f(x)

a = c
x = lambda x: x*x
print(x)

def main():
    if x == True:
        return 1 / 0

if __name__ == "__main__":
    print(x if sys.argv[0] == "hi" else y)

def gen(x: int, y: str):
    for a in range(0, y):
        yield print(y * a)

array = np.mean([1, 2, 3]) * 0.1
""",
True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    # regex statistics
    problems = []
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(a),  # 5
        negz(a),  # 6
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(a),  # 5
        negz(a),  # 6
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(Sym("=")),  # 11
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(Sym("=")),  # 11
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(Sym("=")),  # 11
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(Sym("=")),  # 16
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(d),  # 17
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        identifier, # 18
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        negz(alt(a, d)),  # 18
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        con(Sym("\""), con(rep(alt(stringcontent, constr("\\\""))), Sym("\"")))  # string 19
    ]
    lookaheads = [
        All,  # 19
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # relation 16
        con(alt(Sym("0"), con(nz, rep(d))), opt(con(Sym("."), repp(d)))),  # float number 17
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
        negz(Sym("=")),  # 16
        negz(d),  # 17
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
        altstr("+-*/"),  # operators 14
        repp(w),  # white spaces 15
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
        All,  # 14
        negz(w),  # 15
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
        altstr("(["),  # left brackets 12
        altstr(")]"),  # right brackets 13
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
        All,  # 12
        All,  # 13
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
        Sym(","),  # new argument 9
        Sym("."),  # attribute access 10
        con(opt(altstr("-+*/")), Sym("=")),  # assignment 11
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
        All,  # 9
        All,  # 10
        negz(Sym("=")),  # 11
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
        constr("yield"),  # keyword 6
        Sym("\n"),  # new line 7
        Sym(":"),  # new block 8
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
        negz(a),  # 6
        All,  # 7
        All,  # 8
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))
    regexes = [
        constr("def"),  # keyword 3
        constr("return"),  # keyword 4
        constr("print"),  # keyword 5
    ]
    lookaheads = [
        negz(a),  # 3
        negz(a),  # 4
        negz(a),  # 5
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads, Mode.vague))


def knapsack(algo):
    alpha = lowers + uppers
    a = altstr(lowers + uppers)
    item = lambda x: conls([a for _ in range(x)])
    regexes = [
        item(1)
    ]
    problems = [
        "a", True,
        "asdlf", True,
        "lasdfjldaskjfladksfs", True,
        "aaaaaaaaaaaaaaaaaaaaaaaaaa", True,
        "aldssdfdajdsfasdfjkdsfadskljfdajlkfl", True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(1),
        item(10)
    ]
    problems = [
        "a", True,
        "asdlf", True,
        "lasdfjldaskjfladksfs", True,
        "aaaaaaaaaaaaaaaaaaaaaaaaaa", True,
        "aldssdfdajdsfasdfjkdsfadskljfdajlkfl", True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(2)
    ]
    problems = [
        "aa", True,
        "asdfas", True,
        "a" * 10, True,
        "ab" * 7, True,
        "abcd" * 5, True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(7),
        item(3),
    ]
    problems = [
        "a" * 3, True,
        "a" * 7, True,
        "a" * 9, True,
        "a" * (3+7), True,
        "a" * (3+7), True,
        "a" * (3*2+7*10), True,
        "a" * (3*2+7*0), True,
        "a" * (3*4+7*4), True,
        "a" * (3*4+7*16), True,
        "a" * (3*10+7*1), True,
        "a" * (3*12+7*1), True,
        "a" * (3*11+7*11), True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(7),
        item(9),
        item(3),
    ]
    problems = [
        "a" * 3, True,
        "a" * 7, True,
        "a" * 9, True,
        "a" * (3+7), True,
        "a" * (9+7), True,
        "a" * (3+9+7), True,
        "a" * (3*2+9*1+7*10), True,
        "a" * (3*2+9*11+7*0), True,
        "a" * (3*4+9*2+7*4), True,
        "a" * (3*10+9*10+7*10), True,
        "a" * (3*13+9*10+7*10), True,
        "a" * (3*13+9*15+7*10), True,
        "a" * (3*13+9*15+7*16), True,
        "a" * (3*20+9*15+7*16), True,
        "a" * (3*20+9*19+7*16), True,
        "a" * (3*20+9*19+7*20), True,
        "a" * (3*2+9*19+7*20), True,
        "a" * (3*20+9*1+7*20), True,
        "a" * (3*20+9*19+7*0), True,
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    # regex statistics
    problems = []
    regexes = [
        item(2),
        item(3),
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(2),
        item(4),
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    regexes = [
        item(5),
        item(2),
    ]
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))


def quadratic(algo):
    alpha = "ab"
    regexes = [
        Sym("a"),
        con(rep(Sym("a")), Sym("b")),
    ]
    problems = []
    for x in range(1, 100, 5):
        problems.append("a" * x)
        problems.append(True)
    evaluate(Config(algo, alpha, regexes, problems, None, Mode.vague))
    


if __name__ == "__main__":
    print("Starting evaluation (this might take a while)")
    algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
    artificial = True
    for algo in algos:
        print(f"Evaluating {algo.value}")
        clear_statistics()
        if algo is Algo.lookahead:
            if artificial:
                quadratic(algo)
            else:
                python_lookahead(algo)
        elif algo is Algo.viable:
            if artificial:
                quadratic(algo)
                # knapsack(algo)
            else:
                arithmetics(algo)
                calculator(algo)
                json(algo)
                xml(algo)
                python(algo)
        else:
            if artificial:
                quadratic(algo)
            else:
                arithmetics(algo)
                calculator(algo)
                json(algo)
                xml(algo)
                python(algo)
        if artificial:
            save_statistics("artificial", algo.value)
        else:
            save_statistics("realistic", algo.value)
    print("Evaluation complete (use plot_statistics.py to plot the results)")
