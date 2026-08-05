class Queue:
    def __init__(self):
        self.data: list[int] = []  # each instance gets its own list
    
    def __repr__(self) -> str:
        """Readable string representation of the queue."""
        return f"Queue({self.data})"

def main():
    print("Queues.")

if __name__ == "__main__":
    main()