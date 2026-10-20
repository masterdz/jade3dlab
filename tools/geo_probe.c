#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

typedef union { uint32_t u; float f; } UF;

static uint32_t rd32(const unsigned char *p) {
    return p[0] | (p[1] << 8) | (p[2] << 16) | ((uint32_t)p[3] << 24);
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: %s <dec>\n", argv[0]); return 1; }
    FILE *f = fopen(argv[1], "rb");
    fseek(f, 0, SEEK_END); long sz = ftell(f); fseek(f, 0, SEEK_SET);
    unsigned char *buf = malloc(sz);
    fread(buf, 1, sz, f); fclose(f);

    size_t pos = 0;
    long blk = 0;
    while (pos + 8 <= (size_t)sz) {
        unsigned char *sep = NULL;
        for (size_t i = pos; i + 4 <= (size_t)sz; i++)
            if (buf[i]==0x99 && buf[i+1]==0xC0 && buf[i+2]==0xFF && buf[i+3]==0xEE) { sep = buf+i; break; }
        size_t blen = sep ? (size_t)(sep-(buf+pos)) : (size_t)sz-pos;
        if (blen >= 8) {
            uint32_t hash = rd32(buf+pos);
            uint32_t type = rd32(buf+pos+4);
            if (type == 1) {
                printf("block %ld: mesh hash=%08X len=%zu\n", blk, hash, blen);
                const unsigned char *d = buf+pos+8;
                size_t dl = blen-8;
                for (size_t off = 0; off+4 <= dl && off < 64; off += 4) {
                    uint32_t v = rd32(d+off);
                    UF u; u.u = v;
                    printf("  +%02zu: %08X  %g\n", off, v, u.f);
                }
            }
        }
        if (!sep) break;
        pos = (size_t)(sep-buf)+4;
        blk++;
    }
    free(buf);
    return 0;
}
