import json
from llm.tiamat import Tiamat
from datetime import datetime

EXPECTED_DATASET_JSON = '''
{
    "name": "Example dataset",
    "config": {
        "example_outputs": true
    },
    "data": [
        {
            "input": "What is a pointer?",
            "code": "int var = 2;\nint* ptr = &var;",
            "output": "A pointer is a memory address.",
        }
    ]
}
'''

# Given JSON representing a dataset, run the data through the LLM and return a list of test cases
def get_actual_outputs_from_dataset(json_str):
    json_data = dict(json.loads(json_str))
    config = json_data["config"]
    tiamat = Tiamat()

    json_data["test_ran_at"] = datetime.now().isoformat()

    for data_point in json_data["data"]:
        if not "input" in data_point:
            raise ValueError("Missing 'input' key in data point.")
        
        if not "code" in data_point:
            raise ValueError("Missing 'code' key in data point.")
        
        if config["example_outputs"] and not "output" in data_point:
            raise ValueError("Missing 'output' key in data point.")
        
        # Use Tiamat to get the actual output for the given input and code
        tiamat_result = tiamat(message=data_point["input"], code=data_point["code"])
        data_point["actual_output"] = tiamat_result.answer

    return json_data

# Given a filename, read the JSON data from the file and return transformed data with actual outputs
def get_actual_outputs_from_file(filename):
    try:
        file = open(filename)
        data = get_actual_outputs_from_dataset(file.read())
        file.close()

        return data
    except:
        raise IOError("Could not read JSON file")

# Given an input file, generate actual outputs from the inputs in dataset, and write to output file
def get_actual_outputs_file(input_filename, output_filename):
    data = get_actual_outputs_from_file(input_filename)
    
    with open(output_filename, 'w') as outfile:
        json.dump(data, outfile, indent=4)