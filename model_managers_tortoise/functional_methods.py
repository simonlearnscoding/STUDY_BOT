async def async_apply_to_each(func, array, *args, **kwargs):

    """
    Applies a given async function to each element in the array.
    Additional arguments and keyword arguments are passed to the function.
    """
    results = []
    for element in array:
        result = await func(element, *args, **kwargs)
        results.append(result)
    return results
