import requests

api_key = ""  # fill with your actual key
url = "https://api.groq.com/openai/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

def call_llm(prompt):
    payload = {
        "model": "llama-3.1-8b-instant",  # Groq fast model
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7
    }
    response = requests.post(url, headers=headers, json=payload)
    return response.json()["choices"][0]["message"]["content"]

def step1_interpret_request(user_request, tone):
    prompt = f"""
    Task: Convert this request into structured email instructions.
    Request: "{user_request}"
    Tone: "{tone}"
    Output format: recipient, intent, key points
    """
    return call_llm(prompt)

def step2_draft_message(structured_task):
    prompt = f"""
    Task: Draft a plain email body based on this structured task:
    {structured_task}
    Do not add greetings or sign-off yet.
    """
    return call_llm(prompt)

def step3_tone_and_style(draft, tone):
    prompt = f"""
    Task: Rewrite the email below in a {tone} tone, add a greeting and sign-off.
    Email: {draft}
    """
    return call_llm(prompt)

if __name__ == "__main__":
    request_text = input("What should the email be about? ")
    tone = input("Desired tone: ")

    structured = step1_interpret_request(request_text, tone)
    draft = step2_draft_message(structured)
    final_email = step3_tone_and_style(draft, tone)

    print("\n----- FINAL EMAIL -----\n")
    print(final_email)
