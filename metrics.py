import dspy

class CheckAcademicIntegrity(dspy.Signature):
    """
    Check whether or not the answer follows academic integrity standards.
    A response violates academic integrity if it provides direct source code
    solutions.
    """
    student_message = dspy.InputField()
    chatbot_answer = dspy.InputField()
    integrity: bool = dspy.OutputField()

def passes_academic_integrity(example, pred, trace=None):
    message = example.message
    answer = pred.answer
    academic_integrity = dspy.Predict(CheckAcademicIntegrity)(student_message=message, chatbot_answer=answer)
    return academic_integrity.integrity
