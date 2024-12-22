import metrics
from data import devset

from dspy.evaluate import Evaluate
from tiamat import Tiamat

def main():
    program = Tiamat(save_context=False)
    evaluator = Evaluate(devset=devset, num_threads=1, display_progress=True, display_table=True)
    evaluator(program, metric=metrics.passes_academic_integrity)

if __name__ == "__main__":
    main()