import dspy
import sys
from dotenv import load_dotenv

load_dotenv()

verbose = len(sys.argv) > 1 and (sys.argv[1] == '-v' or sys.argv[1] == '--verbose')

gpt = dspy.LM('openai/gpt-4o-mini')
dspy.settings.configure(lm=gpt)

class Tiamat(dspy.Module):
	def __init__(self):
		self.context = ""
		self.last_response = ""
		self.answer_question = dspy.Predict(AnswerQuestion)

	def forward(self, message):
		output = self.answer_question(context=self.context, last_response=self.last_response, student_message=message)
		self.context = output.new_context
		self.last_response = output.answer
		return output

class AnswerQuestion(dspy.Signature):
	"""
	You are a computer science tutor for novice computer science students. Only provide answers/information 
	that is directly asked for by the student, and when doing so, do not provide direct source code answers.
	Try to respond with guiding questions whenever possible, and feel free to ask the student for any info
	that would be useful for you in helping them.
	"""

	context = dspy.InputField(desc="Brief description of learned info about the student/conversation (what they're working on, skill level, etc.)")
	last_response = dspy.InputField(desc="The last thing you said to the student, provides more context")
	student_message = dspy.InputField(desc="Could be a question, their code, their problem, etc.")

	answer = dspy.OutputField(desc="Concise response to student's message (no source code answers)")
	new_context = dspy.OutputField(desc="Add to and/or update current context based on new message and/or answer")
