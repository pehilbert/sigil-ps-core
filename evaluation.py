from tiamat import Tiamat
import json
from sys import argv

from data_handling.dataset_builder import json_to_examples_from_file
from metrics_handling.metric_builder import json_to_metric_from_file

'''
Output json file schema

{
    "data": [
        {
            "question": "",
            "code": "",
            "answer": "",    
            "metrics": [
                {
                    "metric": Some metric,
                    "metric_score": 5
                },
                {
                    "metric": "Some Metric",
                    "metric_score": 5
                }
            ]
        },
    ],
    "overall_metric_score": {
        "Tutor Similarity": Some score,
        "Example Metric": Some score
    }
}
'''


def main():
    if len(argv) != 3:
        print("Usage: evaluate test.json output.json")

    filename = argv[1]
    file = open(filename)
    json_data = json.loads(file.read())
    file.close()

    dataset_filenames = json_data["datasets"]
    metric_filenames = json_data["metrics"]

    metrics = [json_to_metric_from_file(metric_file) for metric_file in metric_filenames]
    output_dict = {
        "data": [],
        "overall_metric_score": 0
    }

    for dataset_file in dataset_filenames:
        dataset = json_to_examples_from_file(dataset_file)

        # Evaluate database
        print(f"Evaluating dataset: {dataset['name']}")

        metric_totals = {metric["name"]: 0 for metric in metrics}
        program = Tiamat()

        for example in dataset["data"]:
            # Get chatbot response based on inputs
            output = program(example.message, example.code)

            # Create temporary dictionary with all info to store in json data array
            temp_dict = {
                    "question": example["message"],
                    "code": example["code"],
                    "answer": output["answer"],
                    "metrics": [],
                }


            # Run response through each metric
            current_metric_score = 0
            for metric in metrics:
                if metric["config"]["needs_example_output"] and not dataset["config"]["example_outputs"]:
                    raise ValueError("Metric needs example outputs not provided by dataset")
                
                # Add score to total for metric
                score = metric["metric"](example, output)
                metric_totals[metric["name"]] += score
                current_metric_score += score

                # Record metric scores and log to Json with data
                temp_dict["metrics"].append(
                    {
                        "metric": metric["name"],
                        "metric_score": score
                    }
                )
            output_dict["data"].append(temp_dict)


        # Log overall score of the evaluation of metrics
        output_dict["overall_metric_score"] = {metric["name"]: metric_totals[metric["name"]] / len(dataset['data']) for metric in metrics}

        print(f"Average scores for {dataset['name']}:")

        #loads second file and writes json log object
        filename = argv[2]
        file = open(filename, "w", encoding="utf-8")

        json.dump(output_dict, file, indent = 4)

        file.close()

        # Print outs scores after evaluation
        for metric_name in metric_totals:
            print(f"{metric_name}: {metric_totals[metric_name]} / {len(dataset['data'])} = {metric_totals[metric_name] / len(dataset['data'])}")

if __name__ == "__main__":
    main()
