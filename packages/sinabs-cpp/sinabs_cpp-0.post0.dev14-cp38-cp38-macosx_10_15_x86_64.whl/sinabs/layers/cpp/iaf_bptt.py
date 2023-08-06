import torch
import numpy as np
from typing import Optional, Union, List, Tuple
import sinabs.layers.iaf_bptt
from sinabs.cpp import iaf

# - Type alias for array-like objects
import sinabs.layers.cpp.iaf_bptt

ArrayLike = Union[np.ndarray, List, Tuple]

window = 1.0


class SpikingLayer(sinabs.layers.iaf_bptt.SpikingLayer):
    def __init__(
        self,
        threshold: float = 1.0,
        threshold_low: Optional[float] = -1.0,
        membrane_subtract: Optional[float] = None,
        batch_size: Optional[int] = None,
        membrane_reset=False,
    ):
        super().__init__(threshold=threshold, threshold_low=threshold_low, membrane_subtract=membrane_subtract, batch_size=batch_size, membrane_reset=membrane_reset)
        self.__doc__ = sinabs.layers.iaf_bptt.SpikingLayer.__doc__
        if membrane_reset:
            raise NotImplementedError("The CPP implementation does not support membrane reset. "
                                      "Please set membrame_reset=False, or use the native implementation in sinabs")

    def forward(self, binary_input: torch.Tensor):
        # Expected input dimensions
        # (batch_size*time_steps, ...)

        # Compute the synaptic current
        syn_out: torch.Tensor = self.synaptic_output(binary_input)

        # Reshape data to appropriate dimensions -> (time, batch, ...)
        if self.batch_size:
            syn_out = syn_out.reshape((self.batch_size, -1, *syn_out.shape[1:])).transpose(0, 1)

        # Ensure the neuron state are initialized
        if self.state.shape != syn_out.shape[1:]:
            self.reset_states(shape=syn_out.shape[1:], randomize=False)

        # Determine no. of time steps from input
        time_steps = len(syn_out)

        all_spikes, state = iaf.forward(syn_out,
                                        self.state,
                                        self.activations,
                                        self.threshold,
                                        self.threshold_low,
                                        self.threshold*window)

        self.state = state
        self.tw = time_steps
        self.activations = all_spikes[-1]
        self.spikes_number = all_spikes.abs().sum()

        if self.batch_size:
            all_spikes = all_spikes.transpose(0, 1).reshape((-1, *all_spikes.shape[2:]))
        return all_spikes

    def __deepcopy__(self, memo=None):
        other = SpikingLayer(
            threshold=self.threshold,
            threshold_low=self.threshold_low,
            membrane_subtract=self._membrane_subtract,
            batch_size=self.batch_size,
            membrane_reset=self.membrane_reset,
        )

        other.state = self.state.detach().clone()
        other.activations = self.activations.detach().clone()

        return other
