from tiamat import Tiamat

chat = Tiamat()

while True:
    message = input("You: ")

    if message.lower().strip() == "bye":
        break

    code = input("Code? (Leave blank if you don't want to provide code) ")
    output = chat(message, code)

    print(f"Tiamat: {output.answer}")
