from llm.tiamat import Tiamat
from dspy import inspect_history

MAX_MSG_LENGTH = 200

chat = Tiamat()
history = []
feedback = []
personalization = ""

def truncate_string(s, max_length) :
    if len(s) > max_length:
        return s[:max_length - 3] + "..."
    
    return s

provide_code = input("Would you like to provide code? (y/n) ").lower() == 'y'
show_history = input("Would you like to display DSPy history? (y/n) ").lower() == 'y'

while True:
    message = input("You: ")

    if message.lower().strip() == "bye":
        break
    
    if provide_code:
        code = input("Code? (Leave blank if you don't want to provide code) ")
    else:
        code = ""

    output = chat(message, code, history, personalization)

    history.append(f"Student: {message}")
    history.append(f"Tiamat: {output.answer}")

    if show_history:
        print("\nDSPy History:\n")
        inspect_history(1)

    print(f"Tiamat: {output.answer}")

    print()
    get_feedback = input("Would you like to provide feedback for this response? (y/n) ").lower() == 'y'
    print()
    
    if get_feedback:
        response = truncate_string(output.answer, MAX_MSG_LENGTH)
        helpful = input("Was this response helpful? (y/n) ").lower() == 'y'
        reason = truncate_string(input("Provide a brief reason for this feedback: "), MAX_MSG_LENGTH)

        if helpful:
            helpful = "Helpful"
        else:
            helpful = "Unhelpful"

        feedback.append(f"Response: {response}\n{helpful}: {reason}")
        feedback_result = chat.get_personalization_from_feedback(feedback, personalization)
        personalization = feedback_result.personalization

        if show_history:
            print("\nDSPy History:\n")
            inspect_history(1)