""" SAX thin-film models """

from __future__ import annotations

import jax.numpy as jnp
from ..core import model


@model(params={"ni": 1.0, "nj": 1.0, "wl": 532.0})
def fresnel_mirror_ij(params):
    """Model a (fresnel) interface between twoo refractive indices

    Args:
        ni: refractive index of the initial medium
        nf: refractive index of the final
        wl: the wavelength of the light
    """
    r_fresnel_ij = (params["ni"] - params["nj"]) / (
        params["ni"] + params["nj"]
    )  # i->j reflection
    t_fresnel_ij = 2 * params["ni"] / (params["ni"] + params["nj"])  # i->j transmission
    r_fresnel_ji = -r_fresnel_ij  # j -> i reflection
    t_fresnel_ji = (1 - r_fresnel_ij ** 2) / t_fresnel_ij  # j -> i transmission
    sdict = {
        ("in0", "in0"): r_fresnel_ij,
        ("in0", "out0"): t_fresnel_ij,
        ("out0", "in0"): t_fresnel_ji,
        ("out0", "out0"): r_fresnel_ji,
    }
    return sdict


@model(params={"ni": 1.0, "di": 500.0, "wl": 532.0})
def propagation_i(params):
    """Model the phase shift acquired as a wave propagates through medium A

    Args:
        ni: refractive index of medium (at wavelength wl)
        di: thickness of layer
        wl: wavelength
    """
    prop_i = jnp.exp(1j * 2 * jnp.pi * params["ni"] / params["wl"] * params["di"])
    sdict = {
        ("in0", "out0"): prop_i,
        ("out0", "in0"): prop_i,
    }
    return sdict


@model(params={"t_amp": jnp.sqrt(0.5), "t_ang": 0.0})
def mirror(params):
    r_complex_val = _r_complex(params["t_amp"], params["t_ang"])
    t_complex_val = _t_complex(params["t_amp"], params["t_ang"])
    sdict = {
        ("in0", "in0"): r_complex_val,
        ("in0", "out0"): t_complex_val,
        ("out0", "in0"): t_complex_val,  # (1 - r_complex_val**2)/t_complex_val, # t_ji
        ("out0", "out0"): r_complex_val,  # -r_complex_val, # r_ji
    }
    return sdict


def _t_complex(t_amp, t_ang):
    return t_amp * jnp.exp(-1j * t_ang)


def _r_complex(t_amp, t_ang):
    r_amp = jnp.sqrt((1.0 - t_amp ** 2))
    r_ang = t_ang - jnp.pi / 2
    return r_amp * jnp.exp(-1j * r_ang)
