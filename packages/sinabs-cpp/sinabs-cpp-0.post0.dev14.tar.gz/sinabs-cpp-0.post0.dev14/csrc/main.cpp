#include "lif.h"
#include "blif.h"
#include "iaf.h"
#include "threshold.h"
#include "bitshift.h"

PYBIND11_MODULE(TORCH_EXTENSION_NAME, m) {
    bind_lif(m);
    bind_blif(m);
    bind_iaf(m);
    bind_threshold(m);
    bind_bitshift(m);
}

