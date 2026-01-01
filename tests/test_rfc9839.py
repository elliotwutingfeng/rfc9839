import pathlib
import pytest
import typing
from rfc9839 import unicode_scalar, xml_character, unicode_assignable, Subset

TEST_DIR = pathlib.Path(__file__).parent

inverse_unicode_scalars = [0xD800, 0xDFFF]  # surrogate pairs
inverse_xml_characters = (
    [
        0x0000,
        0x0008,
    ]  # control characters
    + [
        0x000B,
        0x000C,
    ]  # vertical tab, form feed
    + [
        0x000E,
        0x001F,
    ]  # control characters
    + [
        0xD800,
        0xDFFF,
    ]  # surrogate pairs
    + [
        0xFFFE,
        0xFFFF,
    ]  # noncharacters
)
inverse_unicode_assignables = (
    [
        0x0000,
        0x0008,
    ]  # control characters
    + [
        0x000B,
        0x000C,
    ]  # vertical tab, form feed
    + [
        0x000E,
        0x001F,
        0x007F,
        0x009F,
    ]  # control characters
    + [
        0xD800,
        0xDFFF,
    ]  # control characters
    + [
        0xFDD0,
        0xFDEF,
        0xFFFE,
        0xFFFF,
    ]  # surrogate pairs
    + [
        0x1FFFE,
        0x1FFFF,
        0x2FFFE,
        0x2FFFF,
        0x3FFFE,
        0x3FFFF,
        0x4FFFE,
        0x4FFFF,
        0x5FFFE,
        0x5FFFF,
        0x6FFFE,
        0x6FFFF,
        0x7FFFE,
        0x7FFFF,
        0x8FFFE,
        0x8FFFF,
        0x9FFFE,
        0x9FFFF,
        0xAFFFE,
        0xAFFFF,
        0xBFFFE,
        0xBFFFF,
        0xCFFFE,
        0xCFFFF,
        0xDFFFE,
        0xDFFFF,
        0xEFFFE,
        0xEFFFF,
        0xFFFFE,
        0xFFFFF,
        0x10FFFE,
        0x10FFFF,
    ]  # noncharacters
)


@pytest.mark.parametrize(
    "validator", [unicode_scalar, xml_character, unicode_assignable]
)
def test_empty_inputs(validator: Subset):
    assert validator.is_valid_utf8(b"")
    assert validator.is_valid_string("")


@pytest.mark.parametrize("pair", unicode_scalar.pairs)
def test_valid_scalar_code_points(pair: tuple[int, int]):
    # Test that all code points in our unicode_scalar table are accepted
    for code_point in range(pair[0], pair[1] + 1):
        assert unicode_scalar.is_valid_code_point(code_point)


@pytest.mark.parametrize("code_point", inverse_unicode_scalars + [-1, 0x10FFFF + 1])
def test_invalid_scalar_code_points(code_point: int):
    # Test that surrogate pairs are rejected
    assert not unicode_scalar.is_valid_code_point(code_point)


def test_invalid_scalar_utf8():
    # Test that bytes and str with surrogates are rejected
    bad_utf8 = [0xED, 0xBA, 0xAD]  # U+DEAD
    bad_bytes = b"a" + bytes(bad_utf8) + b"z"
    bad_str = "a\udeadz"
    assert not unicode_scalar.is_valid_utf8(bad_bytes)
    assert not unicode_scalar.is_valid_string(bad_str)


@pytest.mark.parametrize("pair", xml_character.pairs)
def test_valid_xml_code_points(pair: tuple[int, int]):
    # Test that all code points in our xml_character table are accepted
    for code_point in range(pair[0], pair[1] + 1):
        assert xml_character.is_valid_code_point(code_point)


@pytest.mark.parametrize("code_point", inverse_xml_characters + [-1, 0x10FFFF + 1])
def test_invalid_xml_code_points(code_point: int):
    # Test that inverse ranges are rejected
    assert not xml_character.is_valid_code_point(code_point)


def test_invalid_xml_utf8():
    # Test that bytes and str with surrogates are rejected
    bad_utf8 = [0xED, 0xBA, 0xAD]  # U+DEAD
    bad_bytes = b"a" + bytes(bad_utf8) + b"z"
    bad_str = "a\udeadz"
    assert not xml_character.is_valid_utf8(bad_bytes)
    assert not xml_character.is_valid_string(bad_str)


def test_valid_xml_string_and_utf8():
    chars = []
    raw_bytes = bytearray()
    for pair in xml_character.pairs:
        for code_point in (pair[0], pair[1]):
            char = chr(code_point)
            chars.append(char)
            raw_bytes += char.encode("utf-8")
    assert xml_character.is_valid_string("".join(chars))
    assert xml_character.is_valid_utf8(bytes(raw_bytes))


@pytest.mark.parametrize("code_point", inverse_xml_characters)
def test_invalid_xml_string_from_code_point(code_point: int):
    try:
        bad_bytes = b"a" + chr(code_point).encode("utf-8") + b"z"
    except UnicodeEncodeError:  # no surrogates
        return
    assert not xml_character.is_valid_utf8(bad_bytes)
    assert not xml_character.is_valid_string(
        bad_bytes.decode("utf-8", errors="surrogateescape")
    )


@pytest.mark.parametrize("pair", unicode_assignable.pairs)
def test_valid_assignable_code_points(pair: tuple[int, int]):
    # Test that all code points in our unicode_assignable table are accepted
    for code_point in range(pair[0], pair[1] + 1):
        assert unicode_assignable.is_valid_code_point(code_point)


@pytest.mark.parametrize("code_point", inverse_unicode_assignables + [-1, 0x10FFFF + 1])
def test_invalid_assignable_code_points(code_point: int):
    # Test that inverse ranges are rejected
    assert not unicode_assignable.is_valid_code_point(code_point)


def test_invalid_assignable_utf8():
    # Test that bytes and str with surrogates are rejected
    bad_utf8 = [0xED, 0xBA, 0xAD]  # U+DEAD
    bad_bytes = b"a" + bytes(bad_utf8) + b"z"
    bad_str = "a\udeadz"
    assert not unicode_assignable.is_valid_utf8(bad_bytes)
    assert not unicode_assignable.is_valid_string(bad_str)


def test_valid_assignable_string_and_utf8():
    chars = []
    raw_bytes = bytearray()
    for pair in unicode_assignable.pairs:
        for code_point in (pair[0], pair[1]):
            char = chr(code_point)
            chars.append(char)
            raw_bytes += char.encode("utf-8")
    assert unicode_assignable.is_valid_string("".join(chars))
    assert unicode_assignable.is_valid_utf8(bytes(raw_bytes))


@pytest.mark.parametrize("code_point", inverse_unicode_assignables)
def test_invalid_assignable_string_from_code_point(code_point: int):
    try:
        bad_bytes = b"a" + chr(code_point).encode("utf-8") + b"z"
    except UnicodeEncodeError:  # no surrogates
        return
    assert not unicode_assignable.is_valid_utf8(bad_bytes)
    assert not unicode_assignable.is_valid_string(
        bad_bytes.decode("utf-8", errors="ignore")
    )


@pytest.mark.parametrize("filename", ["sample.txt"])
@pytest.mark.parametrize(
    "validator", [unicode_assignable, unicode_scalar, xml_character]
)
def test_valid_sample_utf8(filename: str, validator: Subset):
    with open(TEST_DIR / filename, "rb") as f:
        data = f.read()
    assert validator.is_valid_utf8(data)


@pytest.mark.parametrize("filename", ["sample.txt"])
@pytest.mark.parametrize(
    "validator", [unicode_assignable, unicode_scalar, xml_character]
)
def test_valid_sample_string(filename: str, validator: Subset):
    with open(TEST_DIR / filename, "r", encoding="utf-8", errors="strict") as f:
        data = f.read()
    assert validator.is_valid_string(data)


@pytest.mark.parametrize("filename", ["UTF-8-test.txt"])
@pytest.mark.parametrize(
    "validator", [unicode_assignable, unicode_scalar, xml_character]
)
def test_invalid_sample_utf8(filename: str, validator: Subset):
    with open(TEST_DIR / filename, "rb") as f:
        data = f.read()
    assert not validator.is_valid_utf8(data)


@pytest.mark.parametrize("filename", ["UTF-8-test.txt"])
@pytest.mark.parametrize(
    "validator", [unicode_assignable, unicode_scalar, xml_character]
)
def test_invalid_sample_string(filename: str, validator: Subset):
    with open(TEST_DIR / filename, "rb") as f:
        data = f.read().decode("utf-8", errors="surrogateescape")
    assert not validator.is_valid_string(data)


@pytest.mark.parametrize(
    "validator", [unicode_assignable, unicode_scalar, xml_character]
)
@pytest.mark.parametrize(
    "method,bad_input",
    [
        ("is_valid_code_point", None),
        ("is_valid_code_point", ""),
        ("is_valid_code_point", b""),
        ("is_valid_string", None),
        ("is_valid_string", 42),
        ("is_valid_string", b""),
        ("is_valid_utf8", None),
        ("is_valid_utf8", ""),
        ("is_valid_utf8", 42),
    ],
)
def test_wrong_input_type(validator: Subset, method: str, bad_input: typing.Any):
    with pytest.raises(TypeError):
        getattr(validator, method)(bad_input)


def test_invalid_pairs():
    with pytest.raises(TypeError):
        Subset(None)  # type: ignore
