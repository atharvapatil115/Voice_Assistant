import re 

def preprocess(text):
    text =  text.lower()
    text = re.sub(r'[^a-z0-9\s]', '', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# text = "Hello there !!!!  how are you??  it is a nice day BRO.....  ..."
# print(preprocess(text))