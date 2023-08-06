""" SAX Photonic Integrated Circuit models """

from __future__ import annotations

import jax.numpy as jnp

from ..core import model
from .._typing import PDict


@model(
    params={
        "length": 25e-6,
        "wl": 1.55e-6,
        "wl0": 1.55e-6,
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
    neff = params["neff"]
    dwl = params["wl"] - params["wl0"]
    dneff_dwl = (params["ng"] - params["neff"]) / params["wl0"]
    neff = neff - dwl * dneff_dwl
    phase = 2.0 * jnp.pi * neff * params["length"] / params["wl"]
    transmission = 10 ** (-params["loss"] * params["length"] / 20) * jnp.exp(1j * phase)
    sdict = {
        ("in", "out"): transmission,
        ("out", "in"): transmission,
    }
    return sdict


@model(params={"coupling": 0.5})
def coupler(params: PDict):
    coupling = params["coupling"]
    assert not isinstance(coupling, dict)
    kappa = coupling ** 0.5
    tau = (1 - coupling) ** 0.5
    sdict = {
        ("p0", "p1"): tau,
        ("p1", "p0"): tau,
        ("p2", "p3"): tau,
        ("p3", "p2"): tau,
        ("p0", "p2"): 1j * kappa,
        ("p2", "p0"): 1j * kappa,
        ("p1", "p3"): 1j * kappa,
        ("p3", "p1"): 1j * kappa,
    }
    return sdict
