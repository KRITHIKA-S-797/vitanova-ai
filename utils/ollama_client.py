import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3"

def ask_ollama(prompt):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "num_predict": 220,
                    "temperature": 0.4
                }
            },
            timeout=120
        )
        response.raise_for_status()
        return response.json().get("response", "").strip()

    except requests.exceptions.ConnectionError:
        return "⚠️ Ollama is not running. Run: ollama run llama3"
    except requests.exceptions.Timeout:
        return "⚠️ Ollama is taking too long."
    except Exception as e:
        return f"⚠️ Ollama error: {e}"