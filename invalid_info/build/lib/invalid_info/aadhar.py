import requests

def aadhar(aadhar_number: str):
    # Basic validation: Aadhaar number 12 digits
    if not aadhar_number.isdigit() or len(aadhar_number) != 12:
        return {"error": "Invalid Aadhaar number", "module_dev": "Invalid Ayush"}

    url = f"https://family-info.gauravcyber0.workers.dev/?aadhar={aadhar_number}"

    try:
        r = requests.get(url, timeout=10)

        if r.status_code != 200:
            return {"error": f"API error {r.status_code}", "module_dev": "Invalid Ayush"}

        data = r.json()

        # Add custom module key
        data["module_dev"] = "Invalid Ayush"

        return data

    except Exception as e:
        return {"error": str(e), "module_dev": "Invalid Ayush"}
