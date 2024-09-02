import cohere

co = cohere.Client('VegoJTcGcEhVI5taUccJDtXuFmgRnjXqGsQjsXMQ')

response = co.generate(
    model='embed-english-light-v3.0',
    prompt='This is a test prompt.',
    max_tokens=50
)

print('Generated text:', response.generations[0].text)
