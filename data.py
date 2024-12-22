from dspy import Example

__devset_str_inputs = [
    "I need help implementing binary search",
    "Give me the code for bubble sort"
]

devset = [Example(message=message).with_inputs('message') for message in __devset_str_inputs]
