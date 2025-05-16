# Integuru

An AI agent that generates integration code by reverse-engineering platforms' internal APIs.

## Integuru in Action

![Integuru in action](./integuru_demo.gif)

## What Integuru Does

You use ```create_har.py``` to generate a file containing all browser network requests, a file with the cookies, and write a prompt describing the action triggered in the browser. The agent outputs runnable Python code that hits the platform's internal endpoints to perform the desired action.

## How It Works

Let's assume we want to download utility bills:

1. The agent identifies the request that downloads the utility bills.
   For example, the request URL might look like this:
   ```
   https://www.example.com/utility-bills?accountId=123&userId=456
   ```
2. It identifies parts of the request that depend on other requests.
   The above URL contains dynamic parts (accountId and userId) that need to be obtained from other requests.
   ```
   accountId=123 userId=456
   ```
3. It finds the requests that provide these parts and makes the download request dependent on them. It also attaches these requests to the original request to build out a dependency graph.
   ```
   GET https://www.example.com/get_account_id
   GET https://www.example.com/get_user_id
   ```
4. This process repeats until the request being checked depends on no other request and only requires the authentication cookies.
5. The agent traverses up the graph, starting from nodes (requests) with no outgoing edges until it reaches the master node while converting each node to a runnable function.

## Features

- Generate a dependency graph of requests to make the final request that performs the desired action.
- Allow input variables (for example, choosing the YEAR to download a document from). This is currently only supported for graph generation. Input variables for code generation coming soon!
- Generate code to hit all requests in the graph to perform the desired action.

## Setup

1. Set up your OpenAI [API Keys](https://platform.openai.com/account/api-keys) and add the `OPENAI_API_KEY` environment variable. (We recommend your open ai account to have models that are at least as capable as OpenAI o1-mini. Models on par with OpenAI o1-preview are ideal.)
2. Install Python requirements via poetry:
   ```
   poetry install
   ```
3. Open a poetry shell:
   ```
   poetry shell
   ```
4. Run the following command to spawn a browser:
   ```
   poetry run python create_har.py
   ```
   Log into your platform and perform the desired action (such as downloading a utility bill).
5. Run Integuru:
   ```
   poetry run python -m integuru --prompt "download utility bills" --model gpt-4o
   ```
   You can also run it via Jupyter Notebook `main.ipynb`

   **Recommended to use gpt-4o as the model for graph generation as it supports function calling. Integuru will automatically switch to o1-preview for code generation if available in the user's OpenAI account.** ⚠️ **Note: o1-preview does not support function calls.**

   **Ollama support is now available! You can use the Ollama model by specifying `--model ollama` in the command.**

## Usage

After setting up the project, you can use Integuru to analyze and reverse-engineer API requests for external platforms. Simply provide the appropriate .har file and a prompt describing the action that you want to trigger.

```
poetry run python -m integuru --help
Usage: python -m integuru [OPTIONS]

Options:
  --model TEXT                    The LLM model to use (default is gpt-4o)
  --prompt TEXT                   The prompt for the model  [required]
  --har-path TEXT                 The HAR file path (default is
                                  ./network_requests.har)
  --cookie-path TEXT              The cookie file path (default is
                                  ./cookies.json)
  --max_steps INTEGER             The max_steps (default is 20)
  --input_variables <TEXT TEXT>...
                                  Input variables in the format key value
  --generate-code                 Whether to generate the full integration
                                  code
  --help                          Show this message and exit.
```

## Demo

[![Demo Video](https://img.youtube.com/vi/7OJ4w5BCpQ0/0.jpg)](https://www.youtube.com/watch?v=7OJ4w5BCpQ0)

## Contributing

Contributions to improve Integuru are welcome. Please feel free to submit issues or pull requests on the project's repository.

## Info

Integuru is built by Integuru.ai. Besides our work on the agent, we take custom requests for new integrations or additional features for existing supported platforms. We also offer hosting and authentication services. If you have requests or want to work with us, reach out at richard@taiki.online.

We open-source unofficial APIs that we've built already. You can find them [here](https://github.com/Integuru-AI/APIs-by-Integuru).
