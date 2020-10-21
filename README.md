# Khmer Font Converter | KFC
A library to convert khmer unicode text to limon format and vice versa.
# Installation
```sh
$ pip install kfc
```
# Usage
### Converting Unicode String to Limon Format
```python
from kfc import unicode_to_limon

unicode = "ថ្ងៃខែឆ្នាំកំណើត"
limon = unicode_to_limon(unicode)
print(f"unicode: {unicode} -> limon: {limon}")
```
### Converting Limon String to Unicode Format
```python
from kfc import limon_to_unicode

limon = "éf¶ExqñaMkMeNIt"
unicode = limon_to_unicode(limon)
print(f"limon: {limon} -> unicode: {unicode}")
```