from tiamat import Tiamat
from dspy import inspect_history

chat = Tiamat()

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

    output = chat(message, code)

    print(f"Tiamat: {output.answer}")

    if show_history:
        print("\nDSPy History:\n")
        inspect_history(1)