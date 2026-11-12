import string
import unittest
from collections import Counter

from otp.pad import ALPHABETS, format_groups, generate_pad, generate_symbols, pad_id


class GenerateSymbolsTest(unittest.TestCase):
    def test_length_and_alphabet(self):
        for alphabet in ALPHABETS.values():
            out = generate_symbols(500, alphabet)
            self.assertEqual(len(out), 500)
            self.assertTrue(set(out) <= set(alphabet))

    def test_rejects_bad_input(self):
        with self.assertRaises(ValueError):
            generate_symbols(0)
        with self.assertRaises(ValueError):
            generate_symbols(10, "a")

    def test_two_pads_differ(self):
        self.assertNotEqual(generate_symbols(100), generate_symbols(100))

    def test_digits_roughly_uniform(self):
        counts = Counter(generate_symbols(100_000, string.digits))
        expected = 10_000
        chi_sq = sum((counts[d] - expected) ** 2 / expected for d in string.digits)
        # 9 degrees of freedom. The bound sits past p = 1e-6 so CI does not flake.
        self.assertLess(chi_sq, 50)


class FormatTest(unittest.TestCase):
    def test_grouping(self):
        self.assertEqual(format_groups("1234567890", 5), "12345 67890")

    def test_line_wrap(self):
        out = format_groups("1" * 30, 5, groups_per_line=3)
        self.assertEqual(out.splitlines(), ["11111 11111 11111", "11111 11111 11111"])

    def test_generate_pad_shape(self):
        pad = generate_pad(groups=25, group_size=5)
        lines = pad.splitlines()
        self.assertEqual(len(lines), 3)
        self.assertEqual(sum(len(line.split()) for line in lines), 25)

    def test_pad_id(self):
        ident = pad_id()
        self.assertEqual(len(ident), 8)
        int(ident, 16)


if __name__ == "__main__":
    unittest.main()
