""" SAX Photonic Integrated Circuit models """

from __future__ import annotations

import jax.numpy as jnp

from ..utils import reciprocal
from ..core import model
from .._typing import PDict


@model(
    params={
        "length": 25.0,
        "wl": 1.55,
        "wl0": 1.55,
        "neff": 2.34,
        "ng": 3.4,
        "loss": 0.0,
    },
)
def straight(params):
    """a simple straight waveguide model

    Args:
        wl: wavelength
        neff: waveguide effective index
        ng: waveguide group index (used for linear neff dispersion)
        wl0: center wavelength at which neff is defined
        length: [m] wavelength length
        loss: [dB/m] waveguide loss
    """
    dwl = params["wl"] - params["wl0"]
    dneff_dwl = (params["ng"] - params["neff"]) / params["wl0"]
    neff = params["neff"] - dwl * dneff_dwl
    phase = 2 * jnp.pi * neff * params["length"] / params["wl"]
    transmission = 10 ** (-params["loss"] * params["length"] / 20) * jnp.exp(1j * phase)
    sdict = reciprocal(
        {
            ("in0", "out0"): transmission,
        }
    )
    return sdict


@model(params={"coupling": 0.5})
def coupler(params: PDict):
    coupling = params["coupling"]
    assert not isinstance(coupling, dict)
    kappa = coupling ** 0.5
    tau = (1 - coupling) ** 0.5
    sdict = reciprocal(
        {
            ("in0", "out0"): tau,
            ("in1", "out1"): tau,
            ("in0", "out1"): 1j * kappa,
            ("in1", "out0"): 1j * kappa,
        }
    )
    return sdict
