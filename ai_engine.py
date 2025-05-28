import openai
import os

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY

def extract_tasks_from_text(text):
    prompt = (
        f"Extract and list tasks from the following email or message:\n\n{text}\n\nTasks:"
    )
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.3,
    )
    tasks_text = response.choices[0].text.strip()
    tasks = [task.strip("- ").strip() for task in tasks_text.split("\n") if task.strip()]
    return tasks
