from tiamat import Tiamat
import json
from sys import argv

from data_handling.dataset_builder import json_to_examples_from_file
from metrics_handling.metric_builder import json_to_metric_from_file

def main():
    # TODO: Provide output filename in arguments
    if len(argv) != 2:
        print("Usage: evaluate test.json")

    filename = argv[1]
    file = open(filename)
    json_data = json.loads(file.read())
    file.close()

    dataset_filenames = json_data["datasets"]
    metric_filenames = json_data["metrics"]

    metrics = [json_to_metric_from_file(metric_file) for metric_file in metric_filenames]

    for dataset_file in dataset_filenames:
        dataset = json_to_examples_from_file(dataset_file)

        # TODO: Add a progress bar or something similar to the built in DSPy evaluator
        print(f"Evaluating dataset: {dataset['name']}")

        metric_totals = {metric["name"]: 0 for metric in metrics}
        program = Tiamat()

        for example in dataset["data"]:
            # Get chatbot response based on inputs
            output = program(example.message, example.code)

            # TODO: Log chatbot response to file with example output for reference if provided
            ##

            # Run response through each metric
            for metric in metrics:
                if metric["config"]["needs_example_output"] and not dataset["config"]["example_outputs"]:
                    raise ValueError("Metric needs example outputs not provided by dataset")
                
                # Add score to total for metric
                score = metric["metric"](example, output)
                metric_totals[metric["name"]] += score

                # TODO: Log response's score for metric to file
                ##

        # TODO: Log average scores for each metric to file
        ##

        # TODO: Print a nice summary of test for current dataset to console
        print(f"Average scores for {dataset['name']}:")

        for metric_name in metric_totals:
            print(f"{metric_name}: {metric_totals[metric_name]} / {len(dataset['data'])} = {metric_totals[metric_name] / len(dataset['data'])}")

if __name__ == "__main__":
    main()
