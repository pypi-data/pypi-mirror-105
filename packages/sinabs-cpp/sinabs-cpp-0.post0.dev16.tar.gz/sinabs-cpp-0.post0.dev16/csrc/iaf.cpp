#include "iaf.h"
#include "threshold.h"


torch::autograd::tensor_list iaf_forward(torch::Tensor data,
                       torch::Tensor vmem,
                       torch::Tensor spk_prev,
                       double threshold,
                       double threshold_low,
                       double window)
{
    int time_steps = data.size(0);

    auto options = vmem.options(); // torch::TensorOptions().device(torch::kCPU, 0);
    torch::Tensor out_spikes = torch::zeros_like(data, options);

    auto out = spk_prev;

    for (int t = 0; t < time_steps; ++t)
    {
        // Membrane reset
        vmem = vmem + data[t] - out*threshold;

        // Lower threshold
        vmem = torch::relu(vmem - threshold_low) + threshold_low;

        // Spike generation
        out = ThresholdSubtract::apply(vmem, threshold, window);
        out_spikes[t] = out;

    }
 
    return {out_spikes, vmem};
}

void bind_iaf(pybind11::module_& m) {
    auto submodule = m.def_submodule("iaf", "sinabs.cpp.iaf");
    submodule.def("forward", &iaf_forward, "IAF forward");
}




