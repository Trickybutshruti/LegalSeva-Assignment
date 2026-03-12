from groq import Groq

# ---------------- API ----------------

client = Groq(
    api_key="API KEY"
)

# ---------------- READ CODE ----------------

def read_code(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()


# ---------------- ANALYZE CODE ----------------

def analyze_code(code):

    prompt = f"""
You are an expert software engineer.

Analyze the following Python code and provide:

1. A clear explanation of what the code does
2. Possible bugs or issues
3. Suggestions for improvement
4. Code quality feedback

Python Code:
{code}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )

    return response.choices[0].message.content


# ---------------- MAIN AGENT ----------------

def code_agent():

    file_path = input("Enter Python file path: ")

    print("\nReading code...\n")

    code = read_code(file_path)

    print("Analyzing code with AI...\n")

    report = analyze_code(code)

    print("\n========== AI CODE ANALYSIS ==========\n")

    print(report)


# ---------------- RUN ----------------

if __name__ == "__main__":
    code_agent()