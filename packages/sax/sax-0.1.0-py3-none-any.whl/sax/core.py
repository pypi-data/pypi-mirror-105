""" SAX core """

from __future__ import annotations

from functools import wraps, partial

import jax
import jax.numpy as jnp

from .utils import merge_dicts
from typing import (
    Dict,
    Iterable,
    Optional,
    Tuple,
    Union,
    overload,
)
from ._typing import (
    Model,
    ModelFunc,
    PDict,
    SDict,
)


def circuit(
    instances: Dict[str, Model],
    connections: Dict[str, str],
    ports: Dict[str, str],
    auto_prune: bool = False,
    keep: Optional[Iterable[Tuple[str, str]]] = None,
) -> Model:
    """generate a circuit model for the instance models given

    Args:
        instances: a dictionary with as keys the model names and values
            the model dictionaries.
        connections: a dictionary where both keys and values are strings of the
            form "modelname:portname"
        ports: a dictionary mapping portnames of the form
            "modelname:portname" to new unique portnames
        auto_prune: remove zero-valued connections and connections between non-output ports
            *while* evaluating the circuit SDict. This results in noticeably better
            performance and lower memory usage.  However, it also makes the
            resulting circuit non-jittable!
        keep: output port combinations to keep. All other combinations will be
            removed from the final sdict. Note: only output ports specified as
            *values* in the ports dict will be considered. For any port combination
            given, the reciprocal equivalent will automatically be added. This flag
            can be used in stead of ``auto_prune=True`` with jax.jit if you know in
            advance which port combinations of the sdict you're interested in.

    Returns:
        the circuit model with the given port names.

    Example:
        A simple mzi can be created as follows::

            import sax
            mzi = sax.circuit(
                instances = {
                    "lft": coupler_model,
                    "top": waveguide_model,
                    "btm": waveguide_model,
                    "rgt": coupler_model,
                },
                connections={
                    "lft:out0": "btm:in0",
                    "btm:out0": "rgt:in0",
                    "lft:out1": "top:in0",
                    "top:out0": "rgt:in1",
                },
                ports={
                    "lft:in0": "in0",
                    "lft:in1": "in1",
                    "rgt:out0": "out0",
                    "rgt:out1": "out1",
                },
            )
    """
    instances, connections, ports = _validate_circuit_parameters(
        instances, connections, ports
    )
    params = {k: v.params for k, v in instances.items()}
    funcs = {k: v.func for k, v in instances.items()}

    if keep:
        keep_dict = {min(p1, p2): max(p1, p2) for p1, p2 in keep}
        keep = tuple((p1, p2) for p1, p2 in keep_dict.items())

    def circuit(params, auto_prune=auto_prune, keep=keep):
        sdicts = {name: func(params[name]) for name, func in funcs.items()}
        return evaluate_circuit(
            sdicts, connections, ports, auto_prune=auto_prune, keep=keep
        )

    return model(circuit, params)


def evaluate_circuit(
    instances: Dict[str, SDict],
    connections: Dict[str, str],
    ports: Dict[str, str],
    auto_prune: bool = False,
    keep: Optional[Iterable[Tuple[str, str]]] = None,
):
    """evaluate a circuit for the sdicts (instances) given.

    Args:
        instances: a dictionary with as keys the instance names and values
            the corresponding SDicts.
        connections: a dictionary where both keys and values are strings of the
            form "instancename:portname"
        ports: a dictionary mapping portnames of the form
            "instancename:portname" to new unique portnames
        auto_prune: remove zero-valued connections and connections between
            non-output ports *while* evaluating the circuit SDict. This results in
            noticeably better performance and lower memory usage.  However, it also
            makes the resulting circuit non-jittable!
        keep: output port combinations to keep. All other combinations will be
            removed from the final sdict. Note: only output ports specified as
            *values* in the ports dict will be considered. For any port combination
            given, the reciprocal equivalent will automatically be added. This flag
            can be used in stead of ``auto_prune=True`` with jax.jit if you know in
            advance which port combinations of the sdict you're interested in.

    Returns:
        the circuit model dictionary with the given port names.

    Example:
        The SDict for a very simple mzi can for example be evaluated as follows::

            import sax
            S_mzi = sax.evaluate_circuit(
                instances = {
                    "lft": S_coupler,
                    "top": S_waveguide,
                    "rgt": S_coupler,
                },
                connections={
                    "lft:out0": "rgt:in0",
                    "lft:out1": "top:in0",
                    "top:out0": "rgt:in1",
                },
                ports={
                    "lft:in0": "in0",
                    "lft:in1": "in1",
                    "rgt:out0": "out0",
                    "rgt:out1": "out1",
                },
            )
    """
    float_eps = 2 * jnp.finfo(jnp.zeros(0, dtype=float).dtype).resolution

    if keep:
        keep = set(list(keep) + [(p2, p1) for p1, p2 in keep])

    block_diag = {}
    for name, sdict in instances.items():
        block_diag.update(
            {(f"{name}:{p1}", f"{name}:{p2}"): v for (p1, p2), v in sdict.items()}
        )

    sorted_connections = sorted(connections.items(), key=_connections_sort_key)
    all_connected_instances = {k: {k} for k in instances}
    for k, l in sorted_connections:
        name1, _ = k.split(":")
        name2, _ = l.split(":")

        connected_instances = (
            all_connected_instances[name1] | all_connected_instances[name2]
        )
        for name in connected_instances:
            all_connected_instances[name] = connected_instances

        current_ports = tuple(
            p
            for instance in connected_instances
            for p in set([p for p, _ in block_diag] + [p for _, p in block_diag])
            if p.startswith(f"{instance}:")
        )

        block_diag.update(_interconnect_ports(block_diag, current_ports, k, l))

        for i, j in list(block_diag.keys()):
            is_connected = i == k or i == l or j == k or j == l
            is_in_output_ports = i in ports and j in ports
            if is_connected and not is_in_output_ports:
                del block_diag[i, j]  # we're not interested in these port combinations

    if auto_prune:
        circuit_sdict = {
            (ports[i], ports[j]): v
            for (i, j), v in block_diag.items()
            if i in ports and j in ports and jnp.any(jnp.abs(v) > float_eps)
        }
    elif keep:
        circuit_sdict = {
            (ports[i], ports[j]): v
            for (i, j), v in block_diag.items()
            if i in ports and j in ports and (ports[i], ports[j]) in keep
        }
    else:
        circuit_sdict = {
            (ports[i], ports[j]): v
            for (i, j), v in block_diag.items()
            if i in ports and j in ports
        }
    return circuit_sdict


@overload
def model(func: None = None, params: Optional[PDict] = None) -> partial:
    ...


@overload
def model(func: ModelFunc = None, params: Optional[PDict] = None) -> Model:
    ...


def model(
    func: Optional[ModelFunc] = None, params: Optional[PDict] = None
) -> Union[Model, partial]:
    """create a SAX model from a model function and its parameters

    Args:
        func: the model function to create a model for.
        params: the default parameters belonging to the model function.

    Returns:
        the SAX model function
    """
    if func is None:
        return partial(model, params=params)  # type: ignore

    default_params = params if params is not None else {}

    if isinstance(func, Model):
        default_params = dict(merge_dicts(func.params, default_params))
        func = func.func

    assert func is not None

    @wraps(func)
    def new(params: PDict):
        params = dict(merge_dicts(default_params, params))  # type: ignore
        return func(params)

    return Model(func=new, params=default_params)


def _connections_sort_key(connection):
    """sort key for sorting a connection dictionary

    Args:
        connection of the form '{instancename}:{portname}'
    """
    part1, part2 = connection
    name1, _ = part1.split(":")
    name2, _ = part2.split(":")
    return (min(name1, name2), max(name1, name2))


def _interconnect_ports(block_diag, current_ports, k, l):
    """interconnect two ports in a given model

    Args:
        model: the component for which to interconnect the given ports
        k: the first port name to connect
        l: the second port name to connect

    Returns:
        the resulting interconnected component, i.e. a component with two ports
        less than the original component.

    Note:
        The interconnect algorithm is based on equation 6 in the paper below::

          Filipsson, Gunnar. "A new general computer algorithm for S-matrix calculation
          of interconnected multiports." 11th European Microwave Conference. IEEE, 1981.
    """
    current_block_diag = {}
    for i in current_ports:
        for j in current_ports:
            vij = _calculate_interconnected_value(
                vij=block_diag.get((i, j), 0.0),
                vik=block_diag.get((i, k), 0.0),
                vil=block_diag.get((i, l), 0.0),
                vkj=block_diag.get((k, j), 0.0),
                vkk=block_diag.get((k, k), 0.0),
                vkl=block_diag.get((k, l), 0.0),
                vlj=block_diag.get((l, j), 0.0),
                vlk=block_diag.get((l, k), 0.0),
                vll=block_diag.get((l, l), 0.0),
            )
            current_block_diag[i, j] = vij
    return current_block_diag


@jax.jit
def _calculate_interconnected_value(vij, vik, vil, vkj, vkk, vkl, vlj, vlk, vll):
    """Calculate an interconnected S-parameter value

    Note:
        The interconnect algorithm is based on equation 6 in the paper below::

          Filipsson, Gunnar. "A new general computer algorithm for S-matrix calculation
          of interconnected multiports." 11th European Microwave Conference. IEEE, 1981.
    """
    result = vij + (
        vkj * vil * (1 - vlk)
        + vlj * vik * (1 - vkl)
        + vkj * vll * vik
        + vlj * vkk * vil
    ) / ((1 - vkl) * (1 - vlk) - vkk * vll)
    return result


def _validate_circuit_parameters(
    models: Dict[str, Model], connections: Dict[str, str], ports: Dict[str, str]
) -> Tuple[Dict[str, Model], Dict[str, str], Dict[str, str]]:
    """validate the netlist parameters of a circuit

    Args:
        models: a dictionary with as keys the model names and values
            the model dictionaries.
        connections: a dictionary where both keys and values are strings of the
            form "modelname:portname"
        ports: a dictionary mapping portnames of the form
            "modelname:portname" to new unique portnames

    Returns:
        the validated and possibly slightly modified models, connections and
        ports dictionaries.
    """

    for name, model in models.items():
        assert isinstance(model, Model), f"'{model}' is not a valid SAX Model"

    if not isinstance(connections, dict):
        msg = f"Connections should be a str:str dict or a list of length-2 tuples."
        connections, _connections = {}, connections
        connection_ports = set()
        for conn in _connections:
            connections[conn[0]] = conn[1]
            for port in conn:
                msg = f"Duplicate port found in connections: '{port}'"
                assert port not in connection_ports, msg
                connection_ports.add(port)

    connection_ports = set()
    for connection in connections.items():
        for port in connection:
            msg = f"Connection ports should all be strings. Got: '{port}'"
            assert isinstance(port, str), msg
            msg = f"Connection ports should have format 'modelname:port'. Got: '{port}'"
            assert len(port.split(":")) == 2, msg
            name, _ = port.split(":")
            msg = f"Model '{name}' used in connection "
            msg += f"'{connection[0]}':'{connection[1]}', "
            msg += f"but '{name}' not found in models dictionary."
            assert name in models, msg
            msg = f"Duplicate port found in connections: '{port}'"
            assert port not in connection_ports, msg
            connection_ports.add(port)

    output_ports = set()
    for port, output_port in ports.items():
        msg = f"Ports keys in 'ports' should all be strings. Got: '{port}'"
        assert isinstance(port, str), msg
        msg = f"Port values in 'ports' should all be strings. Got: '{output_port}'"
        assert isinstance(output_port, str), msg
        msg = f"Port keys in 'ports' should have format 'model:port'. Got: '{port}'"
        assert len(port.split(":")) == 2, msg
        msg = f"Port values in 'ports' shouldn't contain a ':'. Got: '{output_port}'"
        assert ":" not in output_port, msg
        msg = f"Duplicate port found in ports or connections: '{port}'"
        assert port not in connection_ports, msg
        name, _ = port.split(":")
        msg = f"Model '{name}' used in output port "
        msg += f"'{port}':'{output_port}', "
        msg += f"but '{name}' not found in models dictionary."
        assert name in models, msg
        connection_ports.add(port)
        msg = f"Duplicate port found in output ports: '{output_port}'"
        assert output_port not in output_ports, msg
        output_ports.add(output_port)

    return models, connections, ports
