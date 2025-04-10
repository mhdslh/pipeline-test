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
    parser.add_argument("--workflow")
    parser.add_argument("--attempt", default="1")
    parser.add_argument("--data")
    
    args = parser.parse_args()
    
    retry = int(args.attempt)
    
    if retry <= 0:
        return

    inputs = {
        "attempt": str(retry-1),
    }
    for k, v in json.loads(args.data).items():
        inputs[k] = v
        print(f"{k}={v}")

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



if __name__ == "__main__":
    main()