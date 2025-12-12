class ListQueue:
    default_capacity = 5

    def __init__(self):
        self.__data =[None] * ListQueue.default_capacity
        self.__size = 0
        self.__front = 0
        self.__end = 0

    def __len__(self):
        return self.__size

    def is_empty(self):
        return self.__size == 0

    def first(self):
        if self.is_empty():
            print('Queue is empty.')
        else:
            return self.__data[self.__front]

    def dequeue(self):
        if self.is_empty():
            print('Queue is empty.')
            return None

        answer = self.__data[self.__front]
        self.__data[self.__front] = None
        self.__front = (self.__front + 1) % ListQueue.default_capacity
        self.__size -= 1
        return answer

    def enqueue(self, e):
        if self.__size == ListQueue.default_capacity:
            print('The queue is full.')
            return None

        self.__data[self.__end] = e
        self.__end = (self.__end + 1) % ListQueue.default_capacity
        self.__size += 1

    def outputQ(self):
        print(self.__data)



# Chemistry function to simulate a reaction
def simulate_reaction(molecule):
    """Simulate a chemical reaction based on molecule type."""
    reaction_products = {
        "H2": "H2O (with O2)",           # Hydrogen reacts with oxygen to form water
        "O2": "O3 (with electricity)",   # Oxygen can form ozone under specific conditions
        "N2": "NH3 (with H2)",           # Nitrogen and hydrogen form ammonia
        "CO2": "C6H12O6 (with H2O)"      # Photosynthesis-like reaction (simplified)
    }
    return reaction_products.get(molecule, "No reaction")

# Example of using the queue for chemical reactions
def chemistry_queue_example():
    # Create a queue to simulate molecules entering the reaction chamber
    molecule_queue = ListQueue()

    # List of molecules entering the chamber in sequence
    molecules = ["H2", "O2", "N2", "CO2", "H2", "O2"]

    # Enqueue each molecule into the queue
    for molecule in molecules:
        molecule_queue.enqueue(molecule)
        print(f"Molecule {molecule} added to the queue.")

    print("\nProcessing molecules in the reaction chamber (FIFO order):")

    # Process each molecule in FIFO order
    while not molecule_queue.is_empty():
        molecule = molecule_queue.dequeue()
        reaction_result = simulate_reaction(molecule)
        print(f"Molecule {molecule} reacted to form: {reaction_result}")

# Run the chemistry queue example
chemistry_queue_example()

###########################################################################################

from collections import deque

class Queue:
    def __init__(self):
        self._data = deque()

    def enqueue(self, item):
        self._data.append(item)  # O(1)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._data.popleft()  # O(1)

    def front(self):
        if self.is_empty():
            raise IndexError("Front from empty queue")
        return self._data[0]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)