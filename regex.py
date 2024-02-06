from dataclasses import dataclass
from functools import reduce
from typing import cast, Iterable, Union


@dataclass(frozen=True)
class Regex:
    pass
Re = Regex


@dataclass(frozen=True)
class Null(Re):
    pass


@dataclass(frozen=True)
class Epsilon(Re):
    pass
Eps = Epsilon


@dataclass(frozen=True)
class Symbol(Re):
    value: Union[str, int]
Sym = Symbol


@dataclass(frozen=True)
class Concatenation(Re):
    left: Re
    right: Re
Con = Concatenation


@dataclass(frozen=True)
class Alternative(Re):
    left: Re
    right: Re
Alt = Alternative


@dataclass(frozen=True)
class Repetition(Re):
    value: Re
Rep = Repetition


@dataclass(frozen=True)
class Negation(Re):
    value: Re
Neg = Negation


def concat(r1: Re, r2: Re) -> Re:
    match (r1, r2):
        case (Null(), _) | (_, Null()):
            return Null()
        case (Eps(), _):
            return r2
        case (_, Eps()):
            return r1
        case (Con(r11, r12), _):
            return Con(r11, concat(r12, r2))
        case _:
            return Con(r1, r2)
con = concat


def alternative(r1: Re, r2: Re) -> Re:
    match (r1, r2):
        case (Null(), _):
            return r2
        case (_, Null()):
            return r1
        case (Alt(r11, r12), _):
            return Alt(r11, alternative(r12, r2))
        case _:
            return Alt(r1, r2)
alt = alternative


def repeat(re: Re) -> Re:
    match re:
        case Null() | Eps():
            return Eps()
        case Rep(r):
            return re
        case _:
            return Rep(re)
rep = repeat


def negate(re: Re) -> Re:
    match re:
        case Neg(r):
            return r
        case _:
            return Neg(re)
neg = negate


def optional(re: Re) -> Re:
    return alternative(re, Eps())
opt = optional


def repeat_plus(re: Re) -> Re:
    return con(re, rep(re))
repp = repeat_plus


def negate_one(re: Re) -> Re:
    return neg(con(re, neg(Null())))
negg = negate_one


def concat_list(rs: Iterable[Re]) -> Re:
    return reduce(lambda out, r: con(out, r), rs, cast(Re, Eps()))
conls = concat_list


def alternative_list(rs: Iterable[Re]) -> Re:
    return reduce(lambda out, r: alt(out, r), rs, cast(Re, Null()))
altls = alternative_list


def concat_string(string: str) -> Re:
    return conls(map(Sym, string))
constr = concat_string


def alternative_string(string: str) -> Re:
    return altls(map(Sym, string))
altstr = alternative_string
