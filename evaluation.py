from dspy.evaluate import Evaluate
from tiamat import Tiamat
import json
from sys import argv

from data_handling.dataset_builder import json_to_examples_from_file
from metrics_handling.metric_builder import json_to_metric_from_file

def main():
    if len(argv) != 2:
        print("Usage: evaluate test.json")

    filename = argv[1]
    file = open(filename)
    json_data = json.loads(file.read())
    file.close()

    dataset_filenames = json_data["datasets"]
    metric_filenames = json_data["metrics"]

    for dataset in dataset_filenames:
        dataset = json_to_examples_from_file(dataset)
        metrics = [json_to_metric_from_file(metric) for metric in metric_filenames]

        for metric in metrics:
            print(f"TESTING DATASET {dataset["name"]} WITH METRIC {metric["name"]}")

            program = Tiamat(save_context=metric["config"]["needs_history"])

            if metric["config"]["needs_example_output"] and not dataset["config"]["example_outputs"]:
                raise ValueError("Metric needs example outputs not provided by dataset")

            evaluator = Evaluate(devset=dataset["data"], num_threads=1, display_progress=True, display_table=True)
            evaluator(program, metric=metric["metric"])

if __name__ == "__main__":
    main()