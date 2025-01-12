def standardize_tuple(value, n, name, allow_zero=False):
    """Transforms non-negative/positive integer/integers into an integer tuple.

    Args:
        value: int or iterable of ints. The value to validate and convert.
        n: int. The size of the tuple to be returned.
        name: string. The name of the argument being validated, e.g. "strides"
            or "kernel_size". This is only used to format error messages.
        allow_zero: bool, defaults to False. A ValueError will raised if zero is
            received and this param is False.

    Returns:
        A tuple of n integers.
    """
    error_msg = (
        f"The `{name}` argument must be a tuple of {n} integers. "
        f"Received {name}={value}"
    )

    if isinstance(value, int):
        value_tuple = (value,) * n
    else:
        try:
            value_tuple = tuple(value)
        except TypeError:
            raise ValueError(error_msg)
        if len(value_tuple) != n:
            raise ValueError(error_msg)
        for single_value in value_tuple:
            try:
                int(single_value)
            except (ValueError, TypeError):
                error_msg += (
                    f"including element {single_value} of "
                    f"type {type(single_value)}"
                )
                raise ValueError(error_msg)

    if allow_zero:
        unqualified_values = {v for v in value_tuple if v < 0}
        req_msg = ">= 0"
    else:
        unqualified_values = {v for v in value_tuple if v <= 0}
        req_msg = "> 0"

    if unqualified_values:
        error_msg += (
            f", including values {unqualified_values}"
            f" that do not satisfy `value {req_msg}`"
        )
        raise ValueError(error_msg)

    return value_tuple


def standardize_padding(value, allow_causal=False):
    if isinstance(value, (list, tuple)):
        return value
    padding = value.lower()
    if allow_causal:
        allowed_values = {"valid", "same", "causal"}
    else:
        allowed_values = {"valid", "same"}
    if padding not in allowed_values:
        raise ValueError(
            "The `padding` argument must be a list/tuple or one of "
            f"{allowed_values}. "
            f"Received: {padding}"
        )
    return padding
