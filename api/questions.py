import requests

def get_trivia_questions(topic, num_questions=5):
    url = f"https://opentdb.com/api.php?amount={num_questions}&type=boolean&category={topic}"
    response = requests.get(url)
    data = response.json()
    return data['results']

def create_quiz(questions):
    quiz = []
    for question in questions:
        quiz.append({
            'question': question['question'],
            'correct_answer': question['correct_answer']
        })
    return quiz

def main():
    topic = input("Enter the topic for the quiz: ")
    num_questions = int(input("Enter the number of questions: "))
    questions = get_trivia_questions(topic, num_questions)
    quiz = create_quiz(questions)
    
    print("\nTrue-False Quiz:")
    for i, q in enumerate(quiz, 1):
        print(f"{i}. {q['question']} (True/False)")

if __name__ == "__main__":
    main()
