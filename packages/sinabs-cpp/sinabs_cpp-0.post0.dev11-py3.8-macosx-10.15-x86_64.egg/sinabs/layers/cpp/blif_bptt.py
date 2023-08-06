import torch
import numpy as np
import torch.nn as nn
from typing import Optional, Union, List, Tuple
from sinabs.cpp import blif

# - Type alias for array-like objects
ArrayLike = Union[np.ndarray, List, Tuple]


# helper functions
def calc_bitshift_decay(tau, dt):
    bitsh = torch.round(torch.log2(tau / dt))
    bitsh[bitsh < 0] = 0
    return bitsh


class SpikingLayer(nn.Module):
    def __init__(
            self,
            tau_mem: float = 10.0,
            tau_syn: torch.Tensor = torch.tensor((5.0,)),
            threshold: float = 1.0,
            window: float = 0.3,
            batch_size: Optional[int] = None,
    ):
        """
        Pytorch implementation of a spiking neuron with learning enabled.
        This class is the base class for any layer that need to implement
        integrate-and-fire operations.

        Parameters:
        -----------
        tau_mem:
            Membrane time constant
        tau_syn:
            Synaptic time constant
        n_syn:
            Number of synapses per neuron
        threshold:
            Spiking threshold of the neuron.
        """
        super().__init__()
        # Initialize neuron states
        self.threshold = threshold
        self.window = window

        if isinstance(tau_mem, torch.Tensor):
            self.tau_mem = tau_mem
        else:
            self.tau_mem = torch.Tensor([tau_mem])

        if isinstance(tau_syn, torch.Tensor):
            self.tau_syn = tau_syn
        else:
            self.tau_syn = torch.Tensor(tau_syn)

        # Blank parameter place holders
        self.register_buffer("vmem", torch.zeros(1))
        self.register_buffer("isyn", torch.zeros(1))

        # Calculate decay rates
        self.register_buffer("dash_mem", calc_bitshift_decay(self.tau_mem, 1).float())
        self.register_buffer("dash_syn", calc_bitshift_decay(self.tau_syn, 1).float())

        self.register_buffer("alpha_mem", torch.exp(-1/self.tau_mem))
        self.register_buffer("alpha_syn", torch.exp(-1/self.tau_syn))

        self.spikes_number = None
        self.n_syn = len(tau_syn)
        self.batch_size = batch_size

    def reset_states(self, shape=None, randomize=False):
        """
        Reset the state of all neurons in this layer
        """

        device = self.vmem.device
        vmem_shape = (shape[0], shape[1])
        isyn_shape = shape
        dash_mem_shape = vmem_shape
        dash_syn_shape = isyn_shape

        if randomize:
            self.vmem = torch.rand(vmem_shape, device=device)
            self.isyn = torch.rand(isyn_shape, device=device)
        else:
            self.vmem = torch.zeros(vmem_shape, device=device)
            self.isyn = torch.zeros(isyn_shape, device=device)

        self.dash_mem = torch.full(size=dash_mem_shape,
                                   fill_value=calc_bitshift_decay(self.tau_mem, 1).item(),
                                   device=device)
        self.dash_syn = torch.zeros(dash_syn_shape, device=device)
        for n in range(self.n_syn):
            self.dash_syn[:, :, n] = calc_bitshift_decay(self.tau_syn, 1).float()[n].item()

        self.alpha_mem = torch.full(size=dash_mem_shape,
                                    fill_value=torch.exp(-1/self.tau_mem).item(),
                                    device=device)
        self.alpha_syn = torch.zeros(dash_syn_shape, device=device)
        for n in range(self.n_syn):
            self.alpha_syn[:, :, n] = torch.exp(-1/self.tau_syn[n]).item()

    def detach(self):
        self.vmem = self.vmem.detach()
        self.isyn = self.isyn.detach()

    def synaptic_output(self, input_spikes: torch.Tensor) -> torch.Tensor:
        """
        This method needs to be overridden/defined by the child class
        Default implementation is pass through

        :param input_spikes: torch.Tensor input to the layer.
        :return:  torch.Tensor - synaptic output current
        """
        return input_spikes

    def forward(self, binary_input: torch.Tensor):
        # expected input dimension: (n_batches*t_sim, n_syn, n_channels)
        # Compute the synaptic current
        syn_out: torch.Tensor = self.synaptic_output(binary_input)

        # Reshape data to appropriate dimensions -> (time, batch, ...)
        if self.batch_size:
            syn_out = syn_out.reshape((self.batch_size, -1, *syn_out.shape[1:])).transpose(0, 1)

        syn_out = syn_out.movedim(-2, -1)  # (t_sim, n_batches, n_channels, n_syn)

        # Ensure the neuron state are initialized
        if not self.isyn.shape == syn_out.shape[1:]:
            self.reset_states(shape=syn_out.shape[1:], randomize=False)

        # Determine no. of time steps from input
        time_steps = len(syn_out)

        all_spikes, vmem_rec, isyn = blif.forward(syn_out,
                                                  self.vmem,
                                                  self.isyn,
                                                  self.dash_mem,
                                                  self.dash_syn,
                                                  self.alpha_mem,
                                                  self.alpha_syn,
                                                  self.threshold,
                                                  self.window,
                                                  True)

        self.vmem_rec = vmem_rec
        self.vmem = vmem_rec[-1]
        self.isyn = isyn
        self.tw = time_steps
        self.activations = all_spikes
        self.n_spikes_out = all_spikes
        self.spikes_number = all_spikes.abs().sum()

        # should return (n_batches*t_sim, n_neurons)
        if self.batch_size:
            all_spikes = all_spikes.transpose(0, 1).reshape((-1, *all_spikes.shape[2:]))
        return all_spikes

    def __deepcopy__(self, memo=None):
        raise NotImplementedError()
