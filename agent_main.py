# agent_main.py

from ddgs import DDGS # type: ignore
import requests
from bs4 import BeautifulSoup
from groq import Groq # type: ignore

# ---------------- CONFIG ----------------

GROQ_API_KEY = "API KEY"

client = Groq(api_key=GROQ_API_KEY)


# ---------------- SEARCH INTERNET ----------------

def search_internet(query, max_results=5):

    print("Searching the internet...\n")

    results = []

    with DDGS() as ddgs:
        for r in ddgs.text(query, max_results=max_results):
            results.append({
                "title": r["title"],
                "link": r["href"]
            })

    return results


# ---------------- SCRAPE WEBPAGE ----------------

def scrape_page(url):

    try:
        headers = {
             "User-Agent": "Mozilla/5.0"
             }

        response = requests.get(url, headers=headers, timeout=10)
       

        soup = BeautifulSoup(response.text, "html.parser")

        paragraphs = soup.find_all("p")

        text = " ".join([p.get_text() for p in paragraphs])

        return text[:500]   # limit tokens

    except:
        return ""


# ---------------- MEMORY COLLECTION ----------------

def collect_memory(search_results):

    memory = ""

    for result in search_results:

        print(f"Reading: {result['title']}")

        content = scrape_page(result["link"])

        memory += f"\nSOURCE: {result['title']}\n"
        memory += content
        memory += "\n"

    return memory


# ---------------- AI ANALYSIS ----------------

def analyze(memory, ceo_name):

    prompt = f"""
You are an AI research agent.

You have collected information about {ceo_name} from multiple internet sources.

Use ONLY the information provided below to create a clear structured report.

If some websites were inaccessible, ignore them and summarize the information that WAS successfully collected.

Information gathered:
{memory}

Create a report with these sections:

1. Background
2. Career and Major Roles
3. Companies Founded or Led
4. Leadership Style
5. Key Achievements
6. Interesting Facts
7. Sources Used

Important:
- Focus on summarizing the collected information.
- Do not say that information was unavailable unless absolutely necessary.
- Provide meaningful insights from the gathered text.
"""

    response = client.chat.completions.create(

        model="llama-3.1-8b-instant",

        messages=[
            {"role": "user", "content": prompt}
        ]

    )

    return response.choices[0].message.content


# ---------------- MAIN AGENT ----------------

def ceo_agent(name):

    query = f"{name} biography leadership achievements"

    search_results = search_internet(query)

    memory = collect_memory(search_results)

    report = analyze(memory, name)

    return report


# ---------------- RUN PROGRAM ----------------

if __name__ == "__main__":

    ceo = input("Enter CEO name: ")

    report = ceo_agent(ceo)

    print("\n\n===== CEO RESEARCH REPORT =====\n")

    print(report)