import openai

# Wprowadź swój klucz API, który uzyskasz na stronie https://platform.openai.com/account/api-keys

# Funkcja do zadawania pytania GPT i uzyskiwania odpowiedzi
def chat_with_gpt(question):
    openai.api_key = api_key

    try:
        # Wysyłanie zapytania do GPT
        response = openai.ChatCompletion.create(
            engine="gpt-4",  # Możesz użyć innej wersji, jeśli chcesz
            prompt=question,
            max_tokens=150,  # Możesz dostosować długość odpowiedzi,
            temperature=0.5
        )

        # Zwrócenie odpowiedzi z GPT
        return response.choices[0].text.strip()

    except Exception as e:
        return f"Error: {str(e)}"


# Program główny
if __name__ == "__main__":
    print("Witaj w ChatGPT! Zadaj pytanie:")
    user_question = input()
    answer = chat_with_gpt(user_question)
    print(f"Odpowiedź GPT: {answer}")