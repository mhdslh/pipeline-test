import argparse
import requests
import time
import json


OWNER = "mhdslh"
REPO = "pipeline-test"
REF = "main" 

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    parser.add_argument("--attempt", default="1")
    parser.add_argument("--workflow")
    parser.add_argument("--dispatch-input")

    # is there any way to add any key value pair dynamically without knowing them in advance?

    args = parser.parse_args()

    print(f"triggered with ${args.attempt}")
    temp = json.loads(args.dispatch_input)
    for k, v in temp.items():
        print(f"====> {k}={v}")

    retry = int(args.attempt)
    
    if retry <= 0:
        return

    inputs = {
        "attempt": str(retry-1),
    }

    for arg in dynamic_input:
        if "=" in arg:
            key, value = arg.split("=", 1)
            print(f"HERE for {key}={value}")
            inputs[key.lstrip("-")] = value

    payload = {
        "ref": REF,
        "inputs": inputs
    }

    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{args.workflow}/dispatches"

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {args.token}"
    }

    print("20sec pause before re-trigger")
    time.sleep(20)

    response = requests.post(url, headers=headers, json=payload)

    print("Status Code:", response.status_code)
    print("Response:", response.text)



if __name__ == "__main__":
    main()