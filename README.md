# RFC9839

![PyPI - Version](https://img.shields.io/pypi/v/rfc9839?style=for-the-badge)
[![Coveralls](https://img.shields.io/coverallsCoverage/github/elliotwutingfeng/rfc9839?logo=coveralls&style=for-the-badge)](https://coveralls.io/github/elliotwutingfeng/rfc9839?branch=main)
[![License](https://img.shields.io/badge/LICENSE-GPL--3.0-GREEN?style=for-the-badge)](LICENSE)

Python library to check for problematic Unicode code points.

Port of [Go library of the same name](https://github.com/timbray/rfc9839).

Based on the Unicode code-point subsets specified in [RFC9839](https://www.rfc-editor.org/rfc/rfc9839.html).

## Usage

```python
from rfc9839 import unicode_scalar, xml_character, unicode_assignable

code_point = 0xFDDA # ARABIC LIGATURE SAD WITH MEEM WITH ALEF MAKSURA FINAL FORM

print(unicode_scalar.is_valid_code_point(code_point)) # True
print(xml_character.is_valid_code_point(code_point)) # True
print(unicode_assignable.is_valid_code_point(code_point)) # False


print(unicode_assignable.is_valid_string(chr(code_point))) # False
print(xml_character.is_valid_utf8(chr(code_point).encode("utf-8"))) # True
```
