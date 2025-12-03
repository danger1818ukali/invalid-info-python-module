import requests

def mobile(number: str):

    if not number.isdigit() or len(number) != 10:
        return {
            "error": "Invalid mobile number",
            "module_dev": "Invalid Ayush"
        }

    url = f"https://num-info-india.gauravcyber0.workers.dev/?mobile={number}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return {
                "error": f"API error {r.status_code}",
                "module_dev": "Invalid Ayush"
            }

        data = r.json()

        # Add your custom key
        data["module_dev"] = "Invalid Ayush"

        return data

    except Exception as e:
        return {
            "error": str(e),
            "module_dev": "Invalid Ayush"
        }
