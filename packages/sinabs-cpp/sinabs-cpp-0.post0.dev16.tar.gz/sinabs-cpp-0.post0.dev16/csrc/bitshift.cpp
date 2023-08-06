#include <torch/extension.h>
#include <iostream>
#include "bitshift.h"

using namespace torch::autograd;

torch::Tensor BitshiftDecay::forward(AutogradContext *ctx, 
                                     torch::Tensor data, 
                                     torch::Tensor dash,
                                     torch::Tensor alpha) {

  int scale = 10000;
  torch::Tensor data_ = data * scale;
  // right shift is difficult to use here
  // as it only works with scalars
  // torch::Tensor dv = (data_.__rshift__(dash));
  // simulate right shift by division with 2 ** dash
  torch::Tensor dv = data_ / dash;
  dv = torch::floor(torch::where(dv == 0, data_.sign(), dv));
  torch::Tensor v = (data_ - dv) / scale;

  ctx->save_for_backward({data, v, alpha});
  return v;
}

tensor_list BitshiftDecay::backward(AutogradContext *ctx, tensor_list grad_outputs) {
  auto saved = ctx->get_saved_variables();
  auto data = saved[0];
  auto v = saved[1];
  auto alpha = saved[2];

  auto grad_output = grad_outputs[0];
  auto grad_input = grad_output * alpha;
  //std::cout << alpha.sizes() << " " << grad_output.sizes() << std::endl;
  //auto grad_input = grad_output * 0.9;
  //grad_input = torch::where(torch::isnan(grad_input), torch::zeros_like(grad_output), grad_input);

  return {grad_input, torch::Tensor(), torch::Tensor()};
}

torch::Tensor BitshiftDecay::apply(torch::Tensor data, 
                                   torch::Tensor dash, 
                                   torch::Tensor alpha) {
    return torch::autograd::Function<BitshiftDecay>::apply(data, dash, alpha);
}


void bind_bitshift(pybind11::module_& m) {
    auto submodule = m.def_submodule("bitshift", "sinabs.cpp.bitshift");
    pybind11::class_<BitshiftDecay>(submodule, "BitshiftDecay")
        .def_static("forward", &BitshiftDecay::forward)
        .def(pybind11::init<>())
        .def_static("backward", &BitshiftDecay::backward)
        .def_static("apply", &BitshiftDecay::apply);
}

