#ifndef DEMO_CUSTOM_API_H
#define DEMO_CUSTOM_API_H

#include <stdint.h>

/* Object-like macros */
#define DEMO_MAGIC 42
#define DEMO_VERSION_STRING "ohos-migration-demo"
#define DEMO_FLAG_MASK 0xFFFFu

/* Function-like macros */
#define DEMO_MAX(a, b) ((a) > (b) ? (a) : (b))
#define DEMO_CLAMP(x, lo, hi) (DEMO_MAX((lo), DEMO_MAX((x), (hi))))
#define DEMO_BYTES(n) ((n) * (int)sizeof(char))

/* Conditional / alternate definitions */
#ifdef DEMO_FORCE_WIDE
#define DEMO_CELL_SIZE 8
#else
#define DEMO_CELL_SIZE 4
#endif

typedef enum demo_color {
    DEMO_RED = 0,
    DEMO_GREEN = 1,
    DEMO_BLUE = 0xFF,
} demo_color;

typedef enum demo_state {
    DEMO_STATE_IDLE = 0,
    DEMO_STATE_BUSY = 1,
    DEMO_STATE_DONE = -1,
} demo_state;

typedef struct DemoPoint {
    float x;
    float y;
} DemoPoint;

typedef struct DemoRect {
    int32_t left;
    int32_t top;
    int32_t width;
    int32_t height;
} DemoRect;

typedef union DemoBits {
    uint32_t u;
    float f;
    int32_t i;
} DemoBits;

typedef void (*demo_void_callback)(void);
typedef int32_t (*demo_int_binop)(int32_t, int32_t);

static const int32_t demo_file_scope_const = 7;
static const char demo_tag_char = 'D';

static inline int custom_magic(void) {
    return DEMO_MAGIC;
}

static inline uint32_t demo_hash_u32(uint32_t x) {
    return x * 2654435761u;
}

static inline double demo_sum(double a, double b) {
    return a + b;
}

static inline float demo_lerp(float a, float b, float t) {
    return a + (b - a) * t;
}

static inline void demo_nop(void) {
}

static inline const char *demo_tag(void) {
    return DEMO_VERSION_STRING;
}

static inline int32_t demo_enum_to_i32(demo_color c) {
    return (int32_t)c;
}

static inline DemoRect demo_make_rect(int32_t l, int32_t t, int32_t w, int32_t h) {
    DemoRect r;
    r.left = l;
    r.top = t;
    r.width = w;
    r.height = h;
    return r;
}

/*
 * HiAppEvent-shaped API behind conditional extern "C" (same pattern as hiappevent.h).
 *
 * - language = C: the preprocessor drops #ifdef __cplusplus … #endif, so there is no
 *   extern "C" / LinkageSpec. Typedef cursors have lexical parent CXCursor_TranslationUnit;
 *   Indexer.getTypedef registers TypedefDef and Kotlin gets typealias demo_on_receive.
 *
 * - language = C++: the linkage block is present; typedef cursors sit under
 *   CXCursor_LinkageSpec. getTypedef returns the underlying type without registering the
 *   name (Indexer.kt: lexical parent != TranslationUnit => return underlying), so
 *   demo_on_receive disappears from klib metadata.
 *
 *   Prototypes inside the block (e.g. demo_set_watcher_on_receive) may also be missing from
 *   the klib in C++ mode — that is not explained by getTypedef; it means those declarations
 *   never produced usable stubs. LibClang’s indexer can skip a declaration before the
 *   callback if USR is absent or the source location is invalid (see CXIndexDataConsumer::
 *   handleDecl in Clang). The Kotlin wrapper can also skip if clang_indexLoc_getFileLocation
 *   does not resolve a CXFile for that CXIdxLoc. demo_after_extern_c_block is outside the
 *   block as a control (TU-scope declarations still bind).
 */
#ifdef __cplusplus
extern "C" {
#endif

typedef struct DemoAppEventGroup DemoAppEventGroup;
typedef struct DemoWatcher DemoWatcher;

typedef void (*demo_on_receive)(
    const char* domain, const struct DemoAppEventGroup* appEventGroups, uint32_t groupLen);

int demo_set_watcher_on_receive(DemoWatcher* watcher, demo_on_receive onReceive);

#ifdef __cplusplus
}
#endif

/* TU scope when language = C++; indexed even if linkage-block prototypes are skipped. */
int demo_after_extern_c_block(int x);

#endif /* DEMO_CUSTOM_API_H */
