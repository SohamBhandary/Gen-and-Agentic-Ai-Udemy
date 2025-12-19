import tiktoken

enc=tiktoken.encoding_for_model("gpt-4o")
text="Het there my name is soham"
print("before tokeinzayions :",text)
tokens=enc.encode(text)
print(tokens)

decode=enc.decode([13418, 1354, 922, 1308, 382, 813, 6595])
print(decode)