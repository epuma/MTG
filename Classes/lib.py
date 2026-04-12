"""Unicode normalisation helpers for MTGJson card data."""

REPLACEMENTS = {
    '\u2014': '-',   # em dash
    '\u2e3a': '-',   # two-em dash
    '\u2212': '-',   # minus sign
    '\xc6':   'AE',
    '\xe9':   'e',
    '\xe0':   'a',
    '\xfa':   'u',
    '\xe2':   'a',
    '\xfb':   'u',
    '\xe1':   'a',
    '\xed':   'i',
    '\xae':   'R',
    '\xf6':   'o',
    '\xfc':   'u',
    '\u2019': "'",
}


def clean_unicode(item):
    """
    Recursively walk dicts/lists and normalise common unicode characters in
    strings to their ASCII-friendly equivalents.  In Python 3 we can keep
    the result as a proper str (no need to encode to bytes).
    """
    if isinstance(item, list):
        result = []
        for element in item:
            if isinstance(element, dict):
                result.append({clean_unicode(k): clean_unicode(v)
                                for k, v in element.items()})
            else:
                result.append(clean_unicode(element))
        return result

    if isinstance(item, dict):
        return {clean_unicode(k): clean_unicode(v) for k, v in item.items()}

    if isinstance(item, str):
        for char, replacement in REPLACEMENTS.items():
            item = item.replace(char, replacement)
        return item

    return item
