from __future__ import annotations


class Subset:
    def __init__(self, pairs: tuple[tuple[int, int], ...]):
        if not (
            isinstance(pairs, tuple)
            and all(
                isinstance(pair, tuple)
                and len(pair) == 2
                and isinstance(pair[0], int)
                and isinstance(pair[1], int)
                for pair in pairs
            )
        ):
            raise TypeError(
                "Expected `pairs` to be of type tuple[tuple[int, int], ...]"
            )
        self.pairs = pairs

    def is_valid_code_point(self, code_point: int) -> bool:
        if not isinstance(code_point, int):
            raise TypeError(f"Expected int, but {code_point.__class__.__name__} found")
        return any(lo <= code_point <= hi for lo, hi in self.pairs)

    def is_valid_string(self, text: str) -> bool:
        if not isinstance(text, str):
            raise TypeError(f"Expected string, but {text.__class__.__name__} found")
        return all(self.is_valid_code_point(ord(char)) for char in text)

    def is_valid_utf8(self, arr: bytes) -> bool:
        if not isinstance(arr, bytes):
            raise TypeError(f"Expected bytes, but {arr.__class__.__name__} found")
        try:
            text = arr.decode("utf-8")
        except UnicodeDecodeError:
            return False
        return self.is_valid_string(text)


# Note that these range pairs are not sorted by numeric order, but by in descending order of
# estimated traffic, as measured by [Tim's](https://github.com/timbray) guesswork. The idea is that you'd like
# to minimize the number of range checks.

unicode_scalar = Subset(
    (
        (0x0, 0xD7FF),  # most of the BMP
        (0xE000, 0x10FFFF),  # mostly astral planes
    )
)
xml_character = Subset(
    (
        (0x20, 0xD7FF),  # most of the BMP
        (0xA, 0xA),  # newline
        (0xE000, 0xFFFD),  # BMP after surrogates
        (0x9, 0x9),  # Tab
        (0xD, 0xD),  # CR
        (0x10000, 0x10FFFF),  # astral planes
    )
)
unicode_assignable = Subset(
    (
        (0x20, 0x7E),  # ASCII
        (0xA, 0xA),  # newline
        (0xA0, 0xD7FF),  # most of the BMP
        (0xE000, 0xFDCF),  # BMP after surrogates
        (0xFDF0, 0xFFFD),  # BMP after noncharacters block
        (0x9, 0x9),  # Tab
        (0xD, 0xD),  # CR
        (0x10000, 0x1FFFD),  # astral planes from here down
        (0x20000, 0x2FFFD),
        (0x30000, 0x3FFFD),
        (0x40000, 0x4FFFD),
        (0x50000, 0x5FFFD),
        (0x60000, 0x6FFFD),
        (0x70000, 0x7FFFD),
        (0x80000, 0x8FFFD),
        (0x90000, 0x9FFFD),
        (0xA0000, 0xAFFFD),
        (0xB0000, 0xBFFFD),
        (0xC0000, 0xCFFFD),
        (0xD0000, 0xDFFFD),
        (0xE0000, 0xEFFFD),
        (0xF0000, 0xFFFFD),
        (0x100000, 0x10FFFD),
        #
    )
)
