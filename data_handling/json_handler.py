from dspy import Example
import json

EXPECTED_DATASET_JSON = '''
{
    "config": {
        "example_outputs": true
    },
    "data": [
        {
            "input": "What is a pointer?",
            "output": "A pointer is..."
        }
    ]
}
'''

def json_to_examples(json_str):
    try:
        json_data = dict(json.loads(json_str))

        if json_data["config"]["example_outputs"]:
            json_data["data"] = [Example(input=data_point["input"], output=data_point["output"]).with_inputs("input") for data_point in json_data["data"]]
        else:
            json_data["data"] = [Example(input=data_point["input"]).with_inputs("input") for data_point in json_data["data"]]

        return json_data
    except:
        raise ValueError("Invalid JSON provided. Expected data format:" + EXPECTED_DATASET_JSON)
    
def json_to_examples_from_file(filename):
    try:
        file = open(filename)
        data = json_to_examples(file.read())
        file.close()

        return data
    except:
        raise IOError("Could not read JSON file")