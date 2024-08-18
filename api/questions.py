import openai
import os

# Set up your OpenAI API key from environment variables
openai.api_key = os.getenv('OPENAI_API_KEY')

def generate_quiz(topic):
    prompt = f"Create a true-false quiz with 5 questions about {topic}. Each question should be educational and informative."
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    
    quiz = response.choices[0].message.content.strip()
    return quiz

# Get user input for the topic
topic = input("Enter the topic for the quiz: ")

# Generate the quiz
quiz = generate_quiz(topic)

# Print the quiz
print("\nHere is your true-false quiz:\n")
print(quiz)
