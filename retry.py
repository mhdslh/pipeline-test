import argparse
import requests
import time



OWNER = "mhdslh"
REPO = "pipeline-test"
REF = "main" 


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--token")
    parser.add_argument("--retry", type=int, default=1)
    parser.add_argument("--workflow")

    args = parser.parse_args()

    if args.retry <= 0:
        return

    inputs = {
        "attempt": args.retry - 1,
    }

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