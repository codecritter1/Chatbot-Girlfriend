import json
from difflib import get_close_matches

def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r', encoding = "utf-8") as file:
        data: dict = json.load(file)
        return data

def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

def find_best_match(user_question: str, questions: list[str]) -> str | None:
    match: list = get_close_matches(user_question, questions, n=1, cutoff=0.6)
    return match[0] if match else None

def get_answer(question: str, knowledge_base: dict) -> str | None:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            return q["answer"]

def bot():
    knowledge_base: dict = load_knowledge_base('knowledge_base.json')
    while True:
        user_input: str = input("You: ")
        if user_input.lower() == "quit":
            break

        # Corrected "questions" -> "question"
        best_match: str | None = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer(best_match, knowledge_base)
            print(f"Bot: {answer}")
        else:
            print("Bot: What should my response be? I don't know the answer to that question.")
            new_answer: str = input("Type what I should say: ")

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledge_base('knowledge_base.json', knowledge_base)
                print("Bot: Aww, thanks for teaching me! I’ll remember this, promise! 💕😊")

if __name__ == "__main__":
    bot()
