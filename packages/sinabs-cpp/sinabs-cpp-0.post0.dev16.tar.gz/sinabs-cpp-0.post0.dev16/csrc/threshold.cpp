#include "threshold.h"

using namespace torch::autograd;

torch::Tensor ThresholdSubtract::forward(AutogradContext *ctx,
                             torch::Tensor data,
                             double threshold,
                             double window) {

  ctx->save_for_backward({data});
  ctx->saved_data["threshold"] = threshold;
  ctx->saved_data["window"] = window;

  data = (data > 0) * torch::floor(data / threshold);
  return data;
}

tensor_list ThresholdSubtract::backward(AutogradContext *ctx, tensor_list grad_outputs) {
  auto saved = ctx->get_saved_variables();
  auto data = saved[0];
  double threshold = ctx->saved_data["threshold"].toDouble();
  double window = ctx->saved_data["window"].toDouble();

  auto grad_output = grad_outputs[0];
  //auto grad_input = grad_output * (data >= (threshold - window)) / threshold;

  auto vmem_shifted = data - threshold / 2;
  auto vmem_periodic = vmem_shifted % threshold;
  auto vmem_below = vmem_shifted * (data < threshold);
  auto vmem_above = vmem_periodic * (data >= threshold);
  auto vmem_new = vmem_above + vmem_below;

  auto spikePdf = torch::exp(-torch::abs(vmem_new - threshold / 2) / (window / threshold)) / threshold;

  return {grad_output * spikePdf, torch::Tensor(), torch::Tensor()};
}


torch::Tensor ThresholdSubtract::apply(torch::Tensor data, double threshold, double window) {
    return torch::autograd::Function<ThresholdSubtract>::apply(data, threshold, window);
}



void bind_threshold(pybind11::module_& m) {
    auto submodule = m.def_submodule("threshold", "sinabs.cpp.threshold");
    pybind11::class_<ThresholdSubtract>(submodule, "ThresholdSubtract")
        .def_static("forward", &ThresholdSubtract::forward)
        .def(pybind11::init<>())
        .def_static("backward", &ThresholdSubtract::backward)
        .def_static("apply", &ThresholdSubtract::apply);
}
