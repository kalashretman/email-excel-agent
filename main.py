def greet(name: str) -> str:
    return f"Hello, {name}! Day 1 of building an AI agent."


def main():
    print(greet("World"))
    project = {"name": "email-excel-agent", "day": 1, "language": "Python"}
    for key, value in project.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()