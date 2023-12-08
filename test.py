import unittest
from nfa import State, Fragment, regex_to_postfix, regex_to_nfa

class TestNFAConstruction(unittest.TestCase):
    def test_concatenation(self):
        # Test concatenation of 'ab'
        postfix_regex = regex_to_postfix("ab.")
        nfa = regex_to_nfa(postfix_regex)
        self.assertTrue(nfa.accepts("ab"))
        self.assertFalse(nfa.accepts("a"))
        self.assertFalse(nfa.accepts("b"))

    def test_alternation(self):
        # Test alternation of 'a|b'
        postfix_regex = regex_to_postfix("a|b|.")
        nfa = regex_to_nfa(postfix_regex)
        self.assertTrue(nfa.accepts("a"))
        self.assertTrue(nfa.accepts("b"))
        self.assertFalse(nfa.accepts("c"))

    def test_kleene_star(self):
        # Test Kleene star of 'a*'
        postfix_regex = regex_to_postfix("a*.")
        nfa = regex_to_nfa(postfix_regex)
        self.assertTrue(nfa.accepts(""))
        self.assertTrue(nfa.accepts("a"))
        self.assertTrue(nfa.accepts("aaaa"))
        self.assertFalse(nfa.accepts("b"))

if __name__ == '__main__':
    unittest.main()
