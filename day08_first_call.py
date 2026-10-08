"""Day 8: the first call to the Claude API from my own code."""

from config import LLM_MODEL
from llm_client import ask


def main() -> None:
    answer = ask("In two sentences: what is an AI agent, and how is it different from a script?")

    print(f"model:  {LLM_MODEL}")
    print(f"answer: {answer.text}")
    print(f"tokens: {answer.input_tokens} in / {answer.output_tokens} out")
    print(f"cost:   ${answer.cost_usd:.6f}")


if __name__ == "__main__":
    main()