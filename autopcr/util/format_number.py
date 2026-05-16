from typing import Literal, Optional

SCALES = {
    '亿': [('亿', 10 ** 8), ('万', 10 ** 4)],
    '万': [('万', 10 ** 4)],
    'b': [('b', 10 ** 9), ('m', 10 ** 6), ('k', 10 ** 3)],
    'm': [('m', 10 ** 6), ('k', 10 ** 3)],
    'k': [('k', 10 ** 3)],
}

def _trim_float(s: str) -> str:
    return s.rstrip('0').rstrip('.') if '.' in s else s

def _add_separator(s: str, val: int, mode: Literal['auto', 'no', 'yes']) -> str:
    if mode == 'no':
        return s

    use_separator = mode == 'yes' or abs(val) >= 100_000
    if not use_separator:
        return s

    if '.' in s:
        int_part, frac_part = s.split('.', 1)
        return f"{int(int_part):,}.{frac_part}"

    return f"{int(s):,}"

def format_number(
    val: int,
    scale: Optional[Literal['k', 'm', 'b', '万', '亿']] = None,
    decimals: int = 2,
    separator: Literal['auto', 'no', 'yes'] = 'auto',
) -> str:
    if scale is None:
        return _add_separator(str(int(val)), val, separator)

    for suffix, div in SCALES[scale]:
        if abs(val) >= div:
            num = val / div
            s = _trim_float(f"{num:.{decimals}f}")
            return _add_separator(s, val, separator) + suffix

    return _add_separator(str(int(val)), val, separator)

