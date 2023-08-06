""" Useful functions for working with SAX. """

from __future__ import annotations

from typing import (
    Any,
    Tuple,
    Dict,
)
from ._typing import (
    ComplexFloat,
    PDict,
    SDict,
    is_complex_float,
)


def copy_params(params: PDict) -> PDict:
    """copy a parameter dictionary

    Args:
        params: the parameter dictionary to copy

    Returns:
        the copied parameter dictionary

    Note:
        this copy function works recursively on all subdictionaries of the params
        dictionary but does NOT copy any non-dictionary values.
    """
    _params = {}
    for k, v in params.items():
        if isinstance(v, dict):
            _params[k] = copy_params(v)
        elif is_complex_float(v):
            _params[k] = v
        else:
            raise ValueError(
                "params dictionary to copy does not have the right type format"
            )
    return _params


def get_ports(sdict: SDict) -> Tuple[str, ...]:
    """get port names of an sdict

    Args:
        sdict: the SDict dictionary to get the port names from
    """
    ports: Dict[str, Any] = {}
    for key in sdict:
        p1, p2 = key
        ports[p1] = None
        ports[p2] = None
    return tuple(p for p in ports)


def merge_dicts(*dicts: Dict) -> Dict:
    """merge nested dictionaries

    Args:
        *dicts: the dictionaries to merge from left to right, i.e. values in
        dictionaries more to the right get precedence.

    Yields:
        the merged dictionary

    """
    if len(dicts) == 1:
        return dict(_generate_merged_dict(dicts[0], {}))
    elif len(dicts) == 2:
        return dict(_generate_merged_dict(dicts[0], dicts[1]))
    else:
        return merge_dicts(dicts[0], merge_dicts(*dicts[1:]))


def reciprocal(sdict: SDict) -> SDict:
    """Make an SDict reciprocal

    Args:
        sdict: theSDict to make reciprocal

    Returns:
        the reciprocal SDict
    """
    return {
        **{(p1, p2): v for (p1, p2), v in sdict.items()},
        **{(p2, p1): v for (p1, p2), v in sdict.items()},
    }


def rename_ports(sdict: SDict, ports: Dict[str, str]) -> SDict:
    """rename the ports of an SDict

    Args:
        sdict: the SDict to rename the ports for
        ports: a port mapping (dictionary) with keys the old names and values
            the new names.
    """
    original_ports = get_ports(sdict)
    assert len(ports) == len(original_ports)
    return {(ports[p1], ports[p2]): v for (p1, p2), v in sdict.items()}


def set_params(params: PDict, *compnames: str, **kwargs: ComplexFloat) -> PDict:
    """update a parameter dictionary

    add or update the given keyword arguments to each (sub)dictionary of the
    given params dictionary

    Args:
        params: the parameter dictionary to update with the given parameters
        *compnames: the nested component names for which to set the parameters.
            If left out, the given parameters will be applied globally to all
            (sub)components in the dictionary.
        **kwargs: the parameters to update the parameter dictionary with.

    Returns:
        The modified dictionary.

    Note:
        - Even though it's possible to update parameter dictionaries in place,
          this function is convenient to apply certain parameters (e.g.
          wavelength 'wl' or temperature 'T') globally.
        - This operation never updates the given params dictionary inplace.
        - Any non-float keyword arguments will be silently ignored.

    Example:
        This is how to change the wavelength to 1600nm for each component in
        the nested parameter dictionary::

            params = set_params(params, wl=1.6e-6)

        Or to set the temperature for only the direcional coupler named 'dc'
        belonging to the MZI named 'mzi' in the circuit::

            params = set_params(params, "mzi", "dc", T=30.0)
    """
    _params = {}
    if not compnames:
        for k, v in params.items():
            if isinstance(v, dict):
                _params[k] = set_params(v, **kwargs)
            elif is_complex_float(v):
                if k in kwargs and is_complex_float(kwargs[k]):
                    _params[k] = kwargs[k]
                else:
                    _params[k] = v
            else:
                raise ValueError(
                    "params dictionary to set global parameters for "
                    "does not have the right type format"
                )
    else:
        for k, v in params.items():
            if isinstance(v, dict):
                if k == compnames[0]:
                    _params[k] = set_params(v, *compnames[1:], **kwargs)
                else:
                    _params[k] = set_params(v)
            elif is_complex_float(v):
                _params[k] = v
            else:
                raise ValueError(
                    "params dictionary to set global parameters for "
                    "does not have the right type format"
                )
    return _params


def _generate_merged_dict(dict1: Dict, dict2: Dict) -> Dict:
    """merge two (possibly deeply nested) dictionaries

    Args:
        dict1: the first dictionary to merge
        dict2: the second dictionary to merge

    Yields:
        the merged dictionary

    """
    # from https://stackoverflow.com/questions/7204805/how-to-merge-dictionaries-of-dictionaries
    for k in set(dict1.keys()).union(dict2.keys()):
        if k in dict1 and k in dict2:
            if isinstance(dict1[k], dict) and isinstance(dict2[k], dict):
                yield (k, dict(_generate_merged_dict(dict1[k], dict2[k])))  # type: ignore
            else:
                # If one of the values is not a dict, you can't continue merging it.
                # Value from second dict overrides one in first and we move on.
                yield (k, dict2[k])
                # Alternatively, replace this with exception raiser to alert you of value conflicts
        elif k in dict1:
            yield (k, dict1[k])
        else:
            yield (k, dict2[k])
