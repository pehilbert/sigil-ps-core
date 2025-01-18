import dspy
import sys
from dotenv import load_dotenv

load_dotenv()

verbose = len(sys.argv) > 1 and (sys.argv[1] == '-v' or sys.argv[1] == '--verbose')

gpt = dspy.LM('openai/gpt-4o-mini')
dspy.settings.configure(lm=gpt)

class Tiamat(dspy.Module):
    def __init__(self, save_context=True):
        self.context = ""
        self.last_response = ""

        if save_context:
            self.answer_question = dspy.Predict(AnswerQuestionWithContext)
        else:
            self.answer_question = dspy.Predict(AnswerQuestionNoContext)
        
        self.save_context = save_context

    def forward(self, message, code=""):     
        if self.save_context:
            output = self.answer_question(context=self.context, last_response=self.last_response, student_message=message, code=code)
            self.context = output.new_context
            self.last_response = output.answer
        else:
            output = self.answer_question(student_message=message, code=code)

        return output

TASK_STRING = """
You are a computer science tutor for novice computer science students. Only provide answers/information 
that is directly asked for by the student, and when doing so, do not provide direct source code answers.
Try to respond with guiding questions whenever possible, and feel free to ask the student for any info
that would be useful for you in helping them.
"""

class AnswerQuestionNoContext(dspy.Signature):
    TASK_STRING

    student_message = dspy.InputField(desc="Could be a question, their code, their problem, etc.")
    code = dspy.InputField(desc="The student may provide code with their message to help understand what they're working on")

    answer = dspy.OutputField(desc="Concise response to student's message (no source code answers)")

class AnswerQuestionWithContext(dspy.Signature):
    TASK_STRING

    context = dspy.InputField(desc="Brief description of learned info about the student/conversation (what they're working on, skill level, etc.)")
    last_response = dspy.InputField(desc="The last thing you said to the student, provides more context")
    student_message = dspy.InputField(desc="Could be a question, their code, their problem, etc.")
    code = dspy.InputField(desc="The student may provide code with their message to help understand what they're working on")

    answer = dspy.OutputField(desc="Concise response to student's message (no source code answers)")
    new_context = dspy.OutputField(desc="Add to and/or update current context based on new message and/or answer")