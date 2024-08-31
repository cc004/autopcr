import hashlib, base64  

INT_MASK = 0xffffffff
N_HASH = 29
HEADER = b'\x01\x04\x04\x77\x05\x02\x04\x0e\x00\x01\x0f\x70\x77\x70\x00\x0e\x72\x77\x07\x74\x74\x0e\x77\x07\x75\x70\x03\x72\x75\x73\x0e\x72\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36\x36'
TAIL = b'12566690671543B46BC9F74D39582E54'
HEADER2 = b'\x6b\x6e\x6e\x1d\x6f\x68\x6e\x64\x6a\x6b\x65\x1a\x1d\x1a\x6a\x64\x18\x1d\x6d\x1e\x1e\x64\x1d\x6d\x1f\x1a\x69\x18\x1f\x19\x64\x18\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c\x5c'
TAIL2 = b'5D60EFA990727AE5500CAB2CF9BB5F6F'
TABLES = [
    '巴噼叮噜啰铃拉唎啵切咧啪嘭哔卟蹦',
    '啪巴拉铃切噜哔啵啰卟唎嘭叮噼蹦咧',
    '唎啪噼嘭蹦哔拉咧啵卟啰噜巴铃切叮',
    '拉卟噼咧唎叮噜巴切嘭啪哔蹦铃啵啰'
]
HEADER3 = '切噜~'

def sign(text: str, nonce: str) -> str:
    to_hash = (text + nonce).encode('utf8')
    digest = hashlib.sha256(HEADER + to_hash + TAIL).digest()
    digest = hashlib.sha256(HEADER2 + digest).digest()
    b64 = base64.b64encode(digest) + TAIL2

    s = [0x6295C58D, 0x62B82175, 0x7BB0142, 0x6C62272E]

    for bs in b64:
        t, t2 = bs ^ s[0], s[1]
        s[0] = (315 * t) & INT_MASK
        s[1] = (315 * t2 + (s[0] >> 16)) & INT_MASK
        s[2] = (315 * s[2] + (s[1] >> 16) + (t << 24)) & INT_MASK
        s[3] = (315 * s[3] + (s[2] >> 16) + (t2 << 24)) & INT_MASK

    t = (s[0] | (s[1] << 8) if s[2] & 1 else s[2] | (s[3] << 8)) & INT_MASK
    offset = t >> 2
    tableId = offset % 3

    t = 0
    i = 0
    idxs = []

    for x in to_hash + TAIL:
        if i == 0: t = 0
        t = (t << 1) | (x & 1)
        idx = (x & 0xfe) - 1
        i += 1
        if i == 4:
            i = 0
            idxs.append(((t if t else idx) + offset) % 16)
        else:
            idxs.append((idx + offset) % 16)

    n = len(idxs)

    res = [None for _ in range(N_HASH)]

    step = n // N_HASH 

    table = TABLES[tableId]

    for i in range(N_HASH // 2 + 1):
        res[i] = table[idxs[(step * i) % n]]
        res[N_HASH - 1 - i] = table[idxs[(n - 1 - step * i) % n]]

    return HEADER3 + ''.join(res)
