# Efficient Lexical Analysis with Ambiguous Tokens

This project contains different kinds of lexer generators described in the master thesis "Efficient Lexical Analysis with Ambiguous Tokens".

The lexer generators are
- The DFA algorithm: generates DFAs to lex a given string (using longest token selection)
- The MDFA algorithm: generates an MDFA to lex a given string (faster run time)
- The longest match algorithm: generates an MDFA and a match predictor to lex a given string (faster worst case run time)
- The lookahead match algorithm: same as the longest match algorithm but for selecting tokens with lookaheads
- The viable match algorithm: same as the longest match algorithm but for selecting viable tokens, i.e. the longest tokens that still lead to successful tokenizations



Note: in the code we treat DFAs and MDFAs the same i.e. the DFA class is implicitly extended to the definition of an MDFA.
