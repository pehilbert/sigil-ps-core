import json
import dspy
from deepeval.metrics import GEval
from deepeval.test_case import LLMTestCaseParams
from deepeval.test_case import LLMTestCase

EXPECTED_DATA = '''
{
    "name": "Example Metric",
    "config": {
        "needs_history": true,
        "needs_example_output": true
    },
    "metric_description": "How correct the output is",
    "score": {
        "type": "scale",
        "description": "1 is completely incorrect, 5 is completely correct",
        "min": 1,
        "max": 5
    }
}
'''

def json_to_metric(json_str):
    try:
        json_data = json.loads(json_str)

        # Create the GEval metric
        metric = GEval(
            name=json_data["name"],
            criteria=json_data["metric_description"],
            evaluation_steps=[
                json_data["metric_description"]
            ],
            evaluation_params=[
                LLMTestCaseParams.INPUT,
                LLMTestCaseParams.ACTUAL_OUTPUT,
                LLMTestCaseParams.EXPECTED_OUTPUT
            ]
        )

        # Define the evaluation wrapper function
        def evaluate_metric(in_data):

            test_case = LLMTestCase(
                input= in_data["input"],
                actual_output= in_data["code"],
                expected_output= in_data["actual_output"]
            )
            # Evaluate the test cases using the GEval metric
            results = metric.evaluate(test_case)
            return results

        return {
            "name": json_data["name"],
            "config": json_data["config"],
            # "metric": metric,
            "evaluate": evaluate_metric
        }

    except json.JSONDecodeError:
        raise ValueError("Invalid JSON provided. Expected data format:" + EXPECTED_DATA)
    except KeyError as e:
        raise ValueError(f"Missing required key in JSON: {e}")
    
def json_to_metric_from_file(filename):
    try:
        file = open(filename)
        data = json_to_metric(file.read())
        file.close()

        return data
    except:
        raise IOError("Could not read JSON file")
