import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

print("Vocab Size: ", encoder.n_vocab)

text = "I am understanding tokenization."
tokens = encoder.encode(text)

print("Tokens: ", tokens)

print(encoder.decode(tokens))
