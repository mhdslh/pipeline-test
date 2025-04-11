import argparse
import requests
import time
import json

OWNER = "mhdslh"
REPO = "pipeline-test"
REF = "main" 


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Retry a GitHub Actions workflow with updated inputs.")
    parser.add_argument("--token", required=True, help="GitHub personal access token or workflow token")
    parser.add_argument("--retry", default="0", required=True, help="Maximum number of retry attempts left")
    parser.add_argument("--workflow", required=True, help="Workflow file name or ID to dispatch")
    parser.add_argument("--data", required=True, help="JSON string of additional input parameters")
    return parser.parse_args()

def build_inputs(retry: int, data_json: str) -> dict[str, str]:
    try:
        data = json.loads(data_json)
        if not isinstance(data, dict):
            raise ValueError("Parsed data is not a dictionary")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in --data: {e}")

    inputs = {"retry": str(retry - 1)}
    for k, v in data.items():
        inputs[k] = str(v)

    return inputs

def dispatch_workflow(token: str, workflow: str, inputs: dict[str, str]):
    url = f"https://api.github.com/repos/{OWNER}/{REPO}/actions/workflows/{workflow}/dispatches"

    payload = {
        "ref": REF,
        "inputs": inputs,
    }

    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"token {token}",
    }

    print(f"Dispatching workflow '{workflow}' with inputs:")
    for key, value in inputs.items():
        print(f"  {key}: {value}")

    response = requests.post(url, headers=headers, json=payload)

    if not 200 <= response.status_code < 300:
        raise RuntimeError(f"Workflow dispatch failed: {response.status_code} - {response.text}")

    print("Workflow dispatch succeeded.")

def main():    
    args = parse_args()
    
    retry = int(args.retry)
    
    if retry <= 0:
        print("No more retries allowed. Exiting.")
        return

    inputs = build_inputs(retry, args.data)
    dispatch_workflow(args.token, args.workflow, inputs)


if __name__ == "__main__":
    main()