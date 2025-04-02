import json
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
}
'''

def json_to_metric(json_str):
    try:
        json_data = json.loads(json_str)

        # Create the GEval metric object
        metric = GEval(
            name=json_data["name"],
            model="gpt-4o-mini",
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
                actual_output= in_data["actual_output"],
                expected_output= in_data["output"]
            )
            # Evaluate the test cases using the GEval metric
            results = metric.measure(test_case)

            # return scroe found by metric
            return results

        #return the metric data including function to get metric score
        return {
            "name": json_data["name"],
            "config": json_data["config"],
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
