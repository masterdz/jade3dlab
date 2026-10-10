import struct


def lzo_decompress(src: bytes, expected_size: int) -> bytes:
    src_pos = 0
    dst = bytearray()

    if src_pos >= len(src):
        return bytes(dst)

    t = src[src_pos]
    src_pos += 1

    if t > 17:
        t -= 17
        if t < 4:
            return _lzo1x_decompress(src, expected_size)
        for _ in range(t):
            dst.append(src[src_pos])
            src_pos += 1
        t = src[src_pos]
        src_pos += 1

    while True:
        if src_pos >= len(src):
            break

        t = src[src_pos]
        src_pos += 1

        if t >= 64:
            match_len = 1 + ((t >> 5) & 7)
            match_dist = ((t & 0x1f) << 11) + (src[src_pos] << 3) + ((src[src_pos + 1] >> 5) & 7) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
            t = src[src_pos - 1] & 3
            for _ in range(t):
                dst.append(src[src_pos])
                src_pos += 1
        elif t >= 32:
            match_len = (t & 31) + 2
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
        elif t >= 16:
            match_len = (t & 15) + 2
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
        else:
            match_len = t + 3
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1

        if len(dst) >= expected_size:
            break

    return bytes(dst[:expected_size])


def _lzo1x_decompress(src: bytes, expected_size: int) -> bytes:
    src_pos = 0
    dst = bytearray()

    while src_pos < len(src) and len(dst) < expected_size:
        t = src[src_pos]
        src_pos += 1

        if t >= 16:
            match_len = t & 0x0f
            if match_len == 0:
                match_len = src[src_pos]
                src_pos += 1
                while match_len == 0:
                    match_len = src[src_pos]
                    src_pos += 1
                match_len += 15
            match_len += 3

            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2

            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
        elif t >= 8:
            match_len = (t & 0x07) + 2
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
        elif t >= 4:
            match_len = (t & 0x03) + 2
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1
        else:
            match_len = t + 3
            match_dist = ((src[src_pos] << 8) | src[src_pos + 1]) + 1
            src_pos += 2
            match_pos = len(dst) - match_dist
            for _ in range(match_len):
                dst.append(dst[match_pos])
                match_pos += 1

    return bytes(dst[:expected_size])
