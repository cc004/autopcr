"""Decode Taiwan Android PlayerPrefs credentials.

The decoder is intentionally standalone: callers can use ``decode_xml`` for
an upload flow or run this module to produce one TSV row accepted by autopcr.
"""

import argparse
import base64
import re
import struct
from pathlib import Path
from typing import Dict
from urllib.parse import unquote


_PLAYERPREFS_KEY = b'e806f6'


def _xor(data: bytes, key: bytes) -> bytes:
    return bytes(value ^ key[index % len(key)] for index, value in enumerate(data))


def _decode_key(value: str) -> str:
    raw = base64.b64decode(unquote(value))
    return _xor(raw, _PLAYERPREFS_KEY).decode('utf-8')


def _decode_value(key: str, value: str) -> bytes:
    raw = base64.b64decode(unquote(value))
    if len(raw) < 11:
        raise ValueError(f'PlayerPrefs value for {key} is too short')
    trim = 11 if raw[-5] != 0 else 7
    raw = raw[:-trim]
    return _xor(raw, key.encode('utf-8') + _PLAYERPREFS_KEY)


def _decode_udid(raw: bytes) -> str:
    if len(raw) < 4 * 36 + 3:
        raise ValueError('Invalid encrypted UDID')
    return ''.join(chr(raw[4 * index + 6] - 10) for index in range(36))


def _combine_id(values: Dict[str, str], name: str, server_id: int) -> str:
    if name in values:
        value = str(values[name])
    elif f'{name}_lowBits' in values:
        value = str(values[f'{name}_lowBits'])
    else:
        raise ValueError(f'PlayerPrefs is missing {name}')

    high = int(values.get(f'{name}_highBits', '0') or 0)
    if high:
        return str((server_id << 30) | int(value))
    if len(value) == 9:
        return f'{server_id}{value}'
    return value


def decode_xml(content: str) -> Dict[str, str]:
    values: Dict[str, str] = {}
    for match in re.finditer(
        r'<string\s+name="([^"]+)">(.*?)</string>',
        content,
        flags=re.DOTALL,
    ):
        try:
            key = _decode_key(match.group(1))
            raw = _decode_value(key, match.group(2))
        except Exception:
            continue

        if key == 'UDID':
            values[key] = _decode_udid(raw)
        elif len(raw) == 4:
            # PlayerPrefs is little endian on Android.  *_lowBits is unsigned.
            fmt = '<I' if key.endswith(('_lowBits', '_highBits')) else '<i'
            values[key] = str(struct.unpack(fmt, raw)[0])
        else:
            try:
                values[key] = raw.decode('utf-8')
            except UnicodeDecodeError:
                continue

    try:
        server_id = int(values['TW_SERVER_ID'])
    except (KeyError, ValueError) as ex:
        raise ValueError('PlayerPrefs is missing a valid TW_SERVER_ID') from ex
    if server_id not in (1, 2, 3, 4):
        raise ValueError('TW_SERVER_ID must be 1, 2, 3 or 4')

    return {
        **values,
        'TW_SERVER_ID': str(server_id),
        'VIEWER_ID': _combine_id(values, 'VIEWER_ID', server_id),
        'SHORT_UDID': _combine_id(values, 'SHORT_UDID', server_id),
    }


def load_xml(path: str) -> Dict[str, str]:
    return decode_xml(Path(path).read_text(encoding='utf-8'))


def main() -> None:
    parser = argparse.ArgumentParser(
        description='Decode a TW Princess Connect Android PlayerPrefs XML.'
    )
    parser.add_argument('playerprefs')
    parser.add_argument('--alias', default='台服账号')
    args = parser.parse_args()
    info = load_xml(args.playerprefs)
    print('\t'.join((
        args.alias,
        info['SHORT_UDID'],
        info['UDID'],
        '台服',
        info['VIEWER_ID'],
        info['TW_SERVER_ID'],
    )))


if __name__ == '__main__':
    main()
