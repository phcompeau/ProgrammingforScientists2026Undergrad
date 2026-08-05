class Stack:
    def __init__(self):
        # Each stack instance gets its own internal list
        self.data: list[int] = []

    def __repr__(self) -> str:
        """Readable string representation of the stack."""
        return f"Stack({self.data})"


def main():
    print("Stacks.")


if __name__ == "__main__":
    main()