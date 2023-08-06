#include "lif.h"
#include "threshold.h"

torch::autograd::tensor_list lif_forward(torch::Tensor data,
                        torch::Tensor vmem,
                        torch::Tensor isyn,
                        torch::Tensor alpha_mem,
                        torch::Tensor alpha_syn,
                        double threshold,
                        double window,
                        bool record
                        )
{
    int time_steps = data.size(0);
    torch::Tensor vmem_rec;

    auto options = vmem.options();
    // Figure out the shape of vmem
    int64_t * shape = new int64_t[vmem.sizes().size()+1];
    shape[0] = time_steps;

    for (int i = 0; i<vmem.sizes().size(); ++i) {
        shape[i+1] = vmem.size(i);
    }

    auto shape_at = torch::ArrayRef<int64_t>(shape, vmem.sizes().size() + 1);

    torch::Tensor out_spikes = torch::zeros(shape_at, options);

    if (record)
    {
        vmem_rec = torch::zeros(shape_at, options);
        //isyn_rec = torch::zeros(shape_at, options);
    }
    else
    {
        shape[0] = 1;  // Just one time step
        auto shape_at = torch::ArrayRef<int64_t>(shape, vmem.sizes().size() + 1);
        vmem_rec = torch::zeros(shape_at, options);
        //isyn_rec = torch::zeros(shape_at, options);
    }


    for (int t = 0; t < time_steps; ++t)
    {
        // Spike generation
        auto out = ThresholdSubtract::apply(vmem, threshold, window);
        out_spikes[t] = out;

        // Membrane reset
        vmem = vmem - out*threshold;
        if (record)
        {
            // record
            vmem_rec[t] = vmem;
            //isyn_rec[t] = isyn;
        }
        // Do the dynamics
        isyn = isyn + data[t];

        vmem = vmem * alpha_mem;
        isyn = isyn * alpha_syn;

        // State propagation
        vmem = vmem + isyn.sum(-1);

    }
    if (!record)
    {
        // just record the last vmem and isyn
        vmem_rec[0] = vmem;
        //isyn_rec[0] = isyn;
    }


    return {out_spikes, vmem_rec, isyn};
}


torch::autograd::tensor_list lif_inject(torch::Tensor data,
                       torch::Tensor vmem,
                       torch::Tensor isyn,
                       torch::Tensor alpha_mem,
                       torch::Tensor alpha_syn,
                       double threshold,
                       double window)
{
    int time_steps = data.size(0);
    int n_batches = data.size(1);
    int n_neurons = data.size(2);

    auto options = torch::TensorOptions().device(torch::kCPU, 0);
    torch::Tensor out_spikes = torch::ones({time_steps, n_batches, n_neurons}, options);

    for (int t = 0; t < time_steps; ++t)
    {
        // Spike generation
        auto out = ThresholdSubtract::apply(vmem, threshold, window);
        out_spikes[t] = out;

        // Membrane reset
        vmem = vmem - out*threshold;
        vmem = vmem + data[t];

        vmem = vmem * alpha_mem;
    }

    return {out_spikes, vmem, isyn};
}


void bind_lif(pybind11::module_& m) {
    auto submodule = m.def_submodule("lif", "sinabs.cpp.lif");
    submodule.def("forward", &lif_forward, "LIF forward");
    submodule.def("inject", &lif_inject, "LIF inject");
}
