from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .preprocessor import preprocess

COMMANDS = {
    "open browser": "launch_browser",
    "what's the time": "tell_time",
    "tell me a joke": "say_joke",
    "shutdown the system": "shutdown_system",
    "play some music": "play_music",
    "Whats todays date" : "tell_date",
    "Can you Send a Whatsapp message" : "sendMessage"
}
processed_commands = [preprocess(cmd) for cmd in COMMANDS.keys()]


vectorizer = TfidfVectorizer()
vectorizer.fit(processed_commands)

# compare and get the best match

def Calculate_best_match(user_input):
    cleaned_user_input  = preprocess(user_input)

    input_vec = vectorizer.transform([user_input])
    command_vec = vectorizer.transform(processed_commands)

    similarity = cosine_similarity(input_vec,command_vec)[0]

    best_match_index = similarity.argmax()
    best_score = similarity[best_match_index]

    if best_score < 0.3:
        return None,best_score

    best_command = list(COMMANDS.keys())[best_match_index]
    action = COMMANDS[best_command]
    
    return action, best_score

action,score = Calculate_best_match("can you send whatsapp message for me ?")
print(f"Action : {action} \n score: {score}")