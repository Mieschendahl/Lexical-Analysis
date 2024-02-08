# type: ignore
# do not use pytest with this file, just run it with py to test it
from typing import Union, Callable, Any
from generation import *
from lexing import *
from evaluator import *


def test_null(algo) -> None:
    alpha = "ab"
    regexes = [Null()]
    problems = ["", [], "a", []]
    evaluate(Config(algo, alpha, regexes, problems))


def test_epsilon(algo) -> None:
    alpha = "a"
    regexes = [Eps()]
    problems = ["", ["", 0], "a", []]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "ab"
    evaluate(Config(algo, alpha, regexes, problems))


def test_symbol(algo) -> None:
    alpha = "ab"
    regexes = [Sym("a")]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", [],
        "ab", [],
        "ba", [],
        "aa", ["a", 0, "a", 0],
        "aab", [],
        "aaa", ["a", 0, "a", 0, "a", 0]
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [Sym("a"), Sym("b")]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", ["b", 1],
        "ab", ["a", 0, "b", 1],
        "ba", ["b", 1, "a", 0],
        "aa", ["a", 0, "a", 0],
        "bab", ["b", 1, "a", 0, "b", 1],
        "c", [],
        "cb", [],
        "bacb", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_concat(algo) -> None:
    alpha = "ab"
    regexes = [con(Sym("a"), Sym("a"))]
    problems = [
        "", [],
        "a", [],
        "b", [],
        "ab", [],
        "ba", [],
        "aa", ["aa", 0],
        "aaa", [],
        "aaaa", ["aa", 0, "aa", 0],
        "aaaaaa", ["aa", 0, "aa", 0, "aa", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_alternative(algo) -> None:
    alpha = "abc"
    regexes = [alt(Sym("a"), Sym("b"))]
    problems = [
        "", [],
        "a", ["a", 0],
        "b", ["b", 0],
        "ab", ["a", 0, "b", 0],
        "ba", ["b", 0, "a", 0],
        "aa", ["a", 0, "a", 0],
        "bab", ["b", 0, "a", 0, "b", 0],
        "c", [],
        "cb", [],
        "bacb", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_repeat(algo) -> None:
    alpha = "ab"
    regexes = [rep(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "aaa", ["aaa", 0],
        "b", [],
        "ba", [],
        "aaab", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [rep(Sym("a")), rep(Sym("b"))]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "b", ["b", 1],
        "ab", ["a", 0, "b", 1],
        "ba", ["b", 1, "a", 0],
        "aa", ["aa", 0],
        "aabb", ["aa", 0, "bb", 1],
        "bbaa", ["bb", 1, "aa", 0],
        "caabb", [],
        "aabbc", [],
        "bbaac", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_repeat_shortest(algo) -> None:
    alpha = "ab"
    regexes = [rep(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", [],
        "b", [],
        "ba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    alpha = "abc"
    regexes = [rep(Sym("a")), rep(Sym("b"))]
    problems = [
        "", ["", 0],
        "a", [],
        "b", [],
        "ba", [],
        "bbaa", [],
        "bbaac", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_negate(algo) -> None:
    alpha = "ab"
    regexes = [neg(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
        "bb", ["bb", 0],
        "bbba", ["bbba", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(rep(Sym("a")))]
    problems = [
        "", [],
        "a", [],
        "aa", [],
        "aaa", [],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
        "bb", ["bb", 0],
        "bbba", ["bbba", 0]
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(Null())]
    problems = [
        "", ["", 0],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(Eps())]
    problems = [
        "", [],
        "a", ["a", 0],
        "aa", ["aa", 0],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "aaab", ["aaab", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [negg(Sym("a"))]
    problems = [
        "", [],
        "a", [],
        "aa", [],
        "b", ["b", 0],
        "ba", ["ba", 0],
        "ab", [],
        "aaab", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_negate_shortest(algo) -> None:
    alpha = "ab"
    regexes = [neg(Sym("a"))]
    problems = [
        "", ["", 0],
        "a", [],
        "aa", [],
        "b", [],
        "ba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [neg(rep(Sym("a")))]
    problems = [
        "", [],
        "a", [],
        "aa", [],
        "aba", [],
    ]
    evaluate(Config(algo, alpha, regexes, problems))


alpharange = lambda a, b: "".join(map(chr, list(range(ord(a), ord(b) + 1))))
lowers = alpharange("a", "z")
uppers = alpharange("A", "Z")
digits = alpharange("0", "9")
spaces = " \n\t"
specials = "+-*/%=!<>,;(){}[]\"\'"
total = lowers + uppers + digits + spaces + specials


def test_simple(algo) -> None:
    alpha = total
    regexes = [con(Sym("\""), con(rep(altstr(lowers)), Sym("\"")))]
    problems = [
        "", [],
        "a", [],
        "abc", [],
        "''", [],
        "a'b", [],
        "\"'", [],
        "\"\"", ["\"\"", 0],
        "\"\"\"\"", ["\"\"", 0, "\"\"", 0],
        "\"abc\"", ["\"abc\"", 0],
        "\"abc\"\"cba\"", ["\"abc\"", 0, "\"cba\"", 0],
        "\"abc\"abc\"cba\"", []
    ]
    regexes = [
        con(Sym("\""), con(rep(altstr(lowers)), Sym("\""))),
        con(Sym("'"), con(rep(altstr(lowers)), Sym("'")))
    ]
    problems = [
        "", [],
        "a", [],
        "abc", [],
        "''", ["''", 1],
        "a'b", [],
        "\"'", [],
        "\"\"", ["\"\"", 0],
        "\"\"\"\"''''", ["\"\"", 0, "\"\"", 0, "''", 1, "''", 1],
        "'a'", ["'a'", 1],
        "\"abc\"", ["\"abc\"", 0],
        "\"abc\"'cba'", ["\"abc\"", 0, "'cba'", 1],
        "\"abc\"'abc'\"cba\"", ["\"abc\"", 0, "'abc'", 1, "\"cba\"", 0],
        "\"abc\"'abc''cba'\"cba\"", ["\"abc\"", 0, "'abc'", 1, "'cba'", 1, "\"cba\"", 0]
    ]
    evaluate(Config(algo, alpha, regexes, problems))


def test_longest(algo) -> None:
    alpha = total
    regexes = [con(altstr(lowers), rep(alt(altstr(lowers), altstr(digits)))), repp(altstr(digits))]
    problems = [
        "", [],
        "a", ["a", 0],
        "abc", ["abc", 0],
        "b123", ["b123", 0],
        "0", ["0", 1],
        "123", ["123", 1],
        "a0a", ["a0a", 0],
        "00aa00", ["00", 1, "aa00", 0],
        "00A00", []
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [con(negg(Sym("0")), altstr(digits))]
    problems = [
        "0", [],
        "0abc", [],
        "a123", ["a123", 0],
        "abc", [],
        "abc0", ["abc0", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [
        altstr(uppers),
        con(repp(altstr(uppers)), altstr(digits)),
        con(
            altstr(digits),
            con(
                rep(altstr(uppers)),
                con(
                    alt(rep(altstr(uppers)), rep(altstr(digits))),
                    con(rep(altstr(digits)), altstr(uppers))
                )
            )
        )
    ]
    problems = [
        "", [],
        "0", [],
        "a", [],
        "A", ["A", 0],
        "0A", ["0A", 2],
        "A0", ["A0", 1],
        "ABC0", ["ABC0", 1],
        "ABC01", [],
        "0ABCA", ["0ABCA", 2],
        "0ABC123A", ["0ABC123A", 2],
        "0ABC123A1B", ["0ABC123A", 2, "1B", 2],
        "0ABC123A0ABC123A", ["0ABC123A", 2, "0ABC123A", 2],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [
        constr("if"),  # 0
        constr("else"),  # 1
        constr("def"),  # 2
        constr("return"),  # 3
        repp(altstr(spaces)),  # 4
        Sym(","),  # 5,
        Sym(";"),  # 6,
        Sym("="),  # 7
        altstr("({["),  # 8
        altstr(")}]"),  # 9
        alt(Sym("0"), con(altstr("12345679"), rep(altstr(digits)))),  # 10
        con(alt(altstr(lowers), altstr(uppers)), rep(alt(alt(altstr(lowers), altstr(uppers)), altstr(digits)))),  # 11
        alt(altstr("<>"), con(altstr("=!<>"), Sym("="))),  # 12
        altstr("+-*/%")  # 13
    ]
    problems = [
"""
def prob(x) {
    res = 0;
    if (!(x % 10 <= 5)) {
        res = 1;
    }
    return res;
}
""",
[],
"""
def prob(x) {
    res = 0;
    if (x % 10 <= 5) {
        res = 1;
    }
    return res;
}
""",
[
"\n", 4, "def", 2, " ", 4, "prob", 11, "(", 8, "x", 11, ")", 9, " ", 4, "{", 8,
"\n    ", 4, "res", 11, " ", 4, "=", 7, " ", 4, "0", 10, ";", 6,
"\n    ", 4, "if", 0, " ", 4, "(", 8, "x", 11, " ", 4, "%", 13, " ", 4, "10", 10, " ", 4, "<=", 12, " ", 4, "5", 10, ")", 9, " ", 4, "{", 8,
"\n        ", 4, "res", 11, " ", 4, "=", 7, " ", 4, "1", 10, ";", 6,
"\n    ", 4, "}", 9,
"\n    ", 4, "return", 3, " ", 4, "res", 11, ";", 6,
"\n", 4, "}", 9,
"\n", 4
]]
    evaluate(Config(algo, alpha, regexes, problems))
    

def test_lookahead(algo) -> None:
    alpha = total
    regexes = [Sym("a"), Sym("b")]
    lookaheads = [Eps(), Eps()]
    problems = [
        "a", ["a", 0],
        "b", ["b", 1]
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads))
    regexes = [Sym("a"), Sym("b")]
    lookaheads = [con(Sym("b"), All), All]
    problems = [
        "a", [],
        "b", ["b", 1],
        "ab", ["a", 0, "b", 1],
        "ba", [],
        "bb", ["b", 1, "b", 1]
    ]
    regexes = [repp(altstr(lowers)), altstr(digits)]
    lookaheads = [alt(Eps(), con(negg(altstr(lowers)), All)), All]
    problems = [
        "", [],
        "a", ["a", 0],
        "01", ["0", 1, "1", 1],
        "abc", ["abc", 0],
        "abc0", ["abc", 0, "0", 1],
        "aaa0aaa", ["aaa", 0, "0", 1, "aaa", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads))
    evaluate(Config(algo, alpha, regexes, problems, lookaheads))
    regexes = [repp(altstr(lowers)), altstr(digits)]
    lookaheads = [con(repp(altstr(digits)), All), All]
    problems = [
        "", [],
        "a", [],
        "abc", [],
        "0", ["0", 1],
        "b0", ["b", 0, "0", 1],
        "012a", [],
        "0a3", ["0", 1, "a", 0, "3", 1]
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads))
    regexes = [repp(altstr(lowers)), altstr(digits)]
    lookaheads = [con(negg(altstr(lowers)), All), All]
    problems = [
        "", [],
        "a", [],
        "abc", [],
        "0", ["0", 1],
        "b0", ["b", 0, "0", 1],
        "012a", [],
        "0a3", ["0", 1, "a", 0, "3", 1],
        "0a3abc2", ["0", 1, "a", 0, "3", 1, "abc", 0, "2", 1],
        "a-a+", []
    ]
    evaluate(Config(algo, alpha, regexes, problems, lookaheads))


def test_viable(algo) -> None:
    alpha = total
    regexes = [con(Sym("a"), Sym("a")), con(Sym("a"), con(Sym("a"), Sym("a")))]
    problems = [
        "aa", ["aa", 0],
        "aaa", ["aaa", 1],
        "aaaaa", ["aaa", 1, "aa", 0],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [constr("if"), constr("iffalse"), constr("falsefi")]
    problems = [
        "if", ["if", 0],
        "iffalse", ["iffalse", 1],
        "falsefi", ["falsefi", 2],
        "iffalsefi", ["if", 0, "falsefi", 2],
    ]
    evaluate(Config(algo, alpha, regexes, problems))
    regexes = [
        repp(altstr(lowers)),
        repp(altstr(lowers + uppers)),
        con(repp(altstr(uppers)), repp(altstr(digits)))
    ]
    problems = [
        "", [],
        "a", ["a", 0],
        "A", ["A", 1],
        "aA", ["aA", 1],
        "A0", ["A0", 2],
        "aaB0", ["aa", 0, "B0", 2],
        "aaB0aB1aC1", ["aa", 0, "B0", 2, "a", 0, "B1", 2, "a", 0, "C1", 2]
    ]
    evaluate(Config(algo, alpha, regexes, problems))


if __name__ == "__main__":
    print("Starting tests (this might take a while)")
    algos = [Algo.DFA, Algo.MDFA, Algo.longest, Algo.lookahead, Algo.viable]
    for algo in algos:
        print(f"Testing {algo.value}")
        if algo is Algo.lookahead:
            test_null(algo)
            test_epsilon(algo)
            test_symbol(algo)
            test_concat(algo)
            test_alternative(algo)
            test_simple(algo)
            test_repeat_shortest(algo)
            test_negate_shortest(algo)
            test_lookahead(algo)
        elif algo is Algo.viable:
            test_null(algo)
            test_epsilon(algo)
            test_symbol(algo)
            test_concat(algo)
            test_alternative(algo)
            test_simple(algo)
            test_repeat(algo)
            test_negate(algo)
            test_longest(algo)
            test_viable(algo)
        else:
            test_null(algo)
            test_epsilon(algo)
            test_symbol(algo)
            test_concat(algo)
            test_alternative(algo)
            test_simple(algo)
            test_repeat(algo)
            test_negate(algo)
            test_longest(algo)
    print("All tests passed successfully")
