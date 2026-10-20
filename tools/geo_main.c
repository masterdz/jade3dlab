#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>

typedef union { uint32_t u; float f; } UF;

extern uint32_t LOA_ReadULong(char **pp);
extern int32_t LOA_ReadLong(char **pp);
extern int32_t LOA_ReadLong_Ed(char **pp, void *unused);
extern void LOA_ReadVector(char **pp, void *v);
extern void LOA_ReadVector_Ed(char **pp, void *v);
extern uint16_t LOA_ReadUShort(char **pp);
extern int16_t LOA_ReadShort(char **pp);
extern float LOA_ReadFloat(char **pp);
extern void *MEM_GEO_p_Alloc(uint32_t sz);
extern void *MEM_GEO_p_AllocAlign(uint32_t sz, uint32_t align);
extern void MEM_GEO_v_FreeAlign(void *p);
extern void *GEO_pst_Create(LONG nbPts, LONG nbUVs, LONG nbElements, LONG nbColors);
extern void GEO_AllocContent(void *obj);
extern uint32_t GEO_ul_Struct_FullSave(void *obj, char *path, char *name, void *data);

static uint32_t g_type;

void *GRO_Struct_CreateMock(LONG t) { return calloc(1, 1024); }
void *GRO_p_UnknowCreateDefault(void) { return calloc(1, 1024); }
void GRO_Struct_InitMock(void *s, LONG t) {}
void GRO_Struct_FreeMock(void *s) {}

extern void *GEO_P_CreateFromBuffer(void *id, char **buf, void *world);

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
            if (buf[i]==0x99 && buf[i+1]==0xC0 && buf[i+2]==0xFF && buf[i+3]==0x0EE) { sep = buf+i; break; }
        size_t blen = sep ? (size_t)(sep-(buf+pos)) : (size_t)sz-pos;
        if (blen >= 8) {
            uint32_t hash = buf[pos]|(buf[pos+1]<<8)|(buf[pos+2]<<16)|((uint32_t)buf[pos+3]<<24);
            g_type = buf[pos+4]|(buf[pos+5]<<8)|(buf[pos+6]<<16)|((uint32_t)buf[pos+7]<<24);
            if (g_type == 1) {
                printf("block %ld mesh %08X len %zu\n", blk, hash, blen);
                void *id = calloc(1, 128);
                char *p = (char*)(buf + pos + 8);
                void *obj = GEO_P_CreateFromBuffer(id, &p, NULL);
                if (obj) {
                    float *pts = (float*)*(void**)((char*)obj + 8);
                    int npts = *(int*)((char*)obj + 4);
                    printf("  decoded: nbPts=%d\n", npts);
                    for (int i = 0; i < 3 && i < npts; i++)
                        printf("  v[%d]=(%g,%g,%g)\n", i, pts[i*3], pts[i*3+1], pts[i*3+2]);
                } else printf("  decode failed\n");
            }
        }
        if (!sep) break;
        pos = (size_t)(sep-buf)+4;
        blk++;
    }
    free(buf);
    return 0;
}
