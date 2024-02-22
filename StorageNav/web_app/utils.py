import types as tys
import typing as ty
from dataclasses import dataclass
from functools import wraps
from inspect import signature, Parameter

from flask import request, jsonify


@dataclass
class Param:
    name: str
    value_type: ty.Any
    optional: bool
    default: ty.Any | Parameter.empty


def _parse_signature(func):
    params: list[Param] = []
    for param in signature(func).parameters.values():
        optional = False
        if ty.get_origin(param.annotation) in {ty.Union, tys.UnionType}:
            args = ty.get_args(param.annotation)
            value_type = args[0]
            if None in args:
                optional = True
        elif param.annotation is Parameter.empty:
            raise ValueError(f"{param.name} has not annotation of type")
        else:
            value_type = param.annotation

        if value_type not in {str, int, float}:
            raise ValueError(
                f"{param.name} has unsupported type. " "it can be str, int or float"
            )

        default = param.default
        if default is not Parameter.empty:
            optional = True
        if optional and default is Parameter.empty:
            default = None

        params.append(Param(param.name, value_type, optional, default))

    func.__dict__["params"] = params


def parse_args(func):
    _parse_signature(func)

    @wraps(func)
    def _wrapper():
        kwargs: dict[str, ty.Any] = {}
        for param in func.__dict__["params"]:
            value = request.args.get(param.name, Parameter.empty)
            if value is Parameter.empty:
                if not param.optional:
                    return jsonify(
                        status="fail",
                        message=f"required param `{param.name}` not passed",
                    )
                value = Parameter.default
            try:
                value = param.value_type(value)
            except ValueError:
                return jsonify(
                    status="fail", message=f"param `{param.name}` has incorrect type"
                )
            kwargs[param.name] = value

        return func(**kwargs)

    return _wrapper


__all__ = ["parse_args"]
