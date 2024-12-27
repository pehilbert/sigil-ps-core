import json
import dspy

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
        json_data = dict(json.loads(json_str))

        class EvaluationSignature(dspy.Signature):
            f"""
            Given user input and chatbot output, and optionally conversation history
            and/or example output, evaluate the chatbot output based on the following
            description:
            {json_data["metric_description"]}
            """

            input = dspy.InputField()
            chatbot_output = dspy.InputField()
            history = dspy.InputField()
            example_output = dspy.InputField()

            match json_data["score"]["type"].lower():
                case "scale":
                    # description = f"Strictly between {json_data["score"]["min"]} and {json_data["score"]["max"]}; {json_data["score"]["description"]}"
                    score: int = dspy.OutputField(desc=f"Strictly between {json_data["score"]["min"]} and {json_data["score"]["max"]}; {json_data["score"]["description"]}")
                case "boolean":
                    score: bool = dspy.OutputField(desc=json_data["score"]["description"])
                case "percentage":
                    score: float = dspy.OutputField(desc=f"Percentage representing {json_data["score"]["description"]}")
                case _:
                    raise ValueError("Invalid score type")
                
        def metric(example, pred, trace=None):
            input = example.message
            output = example.example_output
            answer = pred.answer
            prediction = dspy.Predict(EvaluationSignature)(
                input=input,
                chatbot_output=answer,
                example_output=output,
                history=trace
            )
            return prediction.score

        return {
            "name": json_data["name"],
            "config": json_data["config"],
            "metric": metric
        }
    
    except:
        raise ValueError("Invalid JSON provided. Expected data format:" + EXPECTED_DATA)
    
def json_to_metric_from_file(filename):
    try:
        file = open(filename)
        data = json_to_metric(file.read())
        file.close()

        return data
    except:
        raise IOError("Could not read JSON file")