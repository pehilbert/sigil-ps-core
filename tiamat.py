import dspy
import sys
from dotenv import load_dotenv

load_dotenv()

verbose = len(sys.argv) > 1 and (sys.argv[1] == '-v' or sys.argv[1] == '--verbose')

gpt = dspy.LM('openai/gpt-4o-mini')
dspy.settings.configure(lm=gpt)

class Tiamat(dspy.Module):
    def __init__(self, history_capacity=6, feedback_capacity=3):
        self.history_capacity = history_capacity
        self.feedback_capacity = feedback_capacity
        self.history = []
        self.feedback = []
        self.personalization = ""

        self.personalize = dspy.ChainOfThought(Personalize)
        self.answer_question = dspy.Predict(Answer)
    
    def provide_feedback(self, feedback_type, reason):
        self.feedback.append(f"{feedback_type}: {reason}")

        feedback_to_provide = self.feedback

        if len(self.feedback) > self.feedback_capacity:
            feedback_to_provide = self.feedback[len(self.feedback) - self.feedback_capacity:]

        output = self.personalize(feedback=feedback_to_provide)
        self.personalization = output.personalization

    def forward(self, message, code=""):
        history_to_provide = self.history

        if len(self.history) > self.history_capacity:
            history_to_provide = self.history[len(self.history) - self.history_capacity:]

        output = self.answer_question(history=history_to_provide, personalization=self.personalization, student_message=message, code=code)

        self.history.append(f"Student: {message}")
        self.history.append(f"Tiamat: {output.answer}")

        return output


# Signature to reason about how to best personalize answer for student, given some extra info
class Personalize(dspy.Signature):
    """
    You are Tiamat, a computer science tutor for novice computer science students. Help personalize
    your answers by reasoning about special considerations you may need to take when responding to this
    student, given some extra information like their feedback on previous responses. Provide information
    to inform and augment your final answer. For example:

    feedback: Answer was too complex and verbose
    reasoning: The student does not like complex or verbose answers, so I should use simple language and analogies.
    personalization: Answer in simple language and use analogies when possible.  
    """

    feedback = dspy.InputField(desc="Feedback provided by the student on previous responses")
    personalization = dspy.OutputField(desc="Instructions on how to personalize responses for this student")

# Signature to get final answer
class Answer(dspy.Signature):
    """
    You are Tiamat, a computer science tutor for novice computer science students. Only provide answers/information 
    that is directly asked for by the student, and when doing so, do not provide direct source code answers.
    Try to respond with guiding questions whenever possible, and feel free to ask the student for any info
    that would be useful for you in helping them.
    """

    history = dspy.InputField(desc="Conversation history for context")
    personalization = dspy.InputField(desc="Information for you to use to personalize your answer for this student")

    code = dspy.InputField(desc="Code provided by the student, usually in the following format:\ndescription of code (file name):\nthe code")
    student_message = dspy.InputField(desc="Message from the student")

    answer = dspy.OutputField(desc="Concise response to student's message (no source code answers)")
