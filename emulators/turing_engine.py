class TuringMachine:
    def __init__(self):
        # Tape is a dictionary — key is position, value is symbol
        # Using dict instead of list gives us infinite tape in both directions
        self.tape = {}
        self.head = 0
        self.state = "q0"
        self.running = False
        self.steps = 0
        self.rules = {}

    def reset(self):
        # Clear everything back to initial state
        self.tape = {}
        self.head = 0
        self.state = "q0"
        self.running = False
        self.steps = 0

    def read(self):
        # Read current cell — blank if never written
        return self.tape.get(self.head, "_")

    def write(self, symbol):
        # Write symbol to current cell
        self.tape[self.head] = symbol

    def move(self, direction):
        # Move head left or right one cell
        if direction == "R":
            self.head += 1
        elif direction == "L":
            self.head -= 1

    def step(self):
        # One fetch-decode-execute cycle
        # Read current symbol
        symbol = self.read()

        # Look up rule for current state + symbol
        key = (self.state, symbol)
        if key not in self.rules:
            # No rule found — machine halts
            self.running = False
            return False

        # Decode the rule
        new_state, write_symbol, direction = self.rules[key]

        # Execute
        self.write(write_symbol)
        self.move(direction)
        self.state = new_state
        self.steps += 1

        # Check if we reached halt state
        if self.state == "halt":
            self.running = False
            return False

        return True

    def load_program(self, name):
        # Load a built-in example program
        self.reset()

        if name == "binary_increment":
            # Increments a binary number on the tape
            # Example: 1 0 1 → 1 1 0
            self.tape = {0: "1", 1: "0", 2: "1"}
            self.head = 2
            self.state = "q0"
            self.rules = {
                # Scan right to find end
                ("q0", "0"): ("q0", "0", "R"),
                ("q0", "1"): ("q0", "1", "R"),
                ("q0", "_"): ("q1", "_", "L"),
                # Increment from right
                ("q1", "1"): ("q1", "0", "L"),
                ("q1", "0"): ("halt", "1", "R"),
                ("q1", "_"): ("halt", "1", "R"),
            }

        elif name == "unary_add":
            # Adds two unary numbers separated by 0
            # Example: 1 1 0 1 1 1 → 1 1 1 1 1
            self.tape = {0: "1", 1: "1", 2: "0", 3: "1", 4: "1", 5: "1"}
            self.head = 0
            self.state = "q0"
            self.rules = {
                # Move right over first number
                ("q0", "1"): ("q0", "1", "R"),
                # Found separator — replace with 1
                ("q0", "0"): ("q1", "1", "R"),
                # Move right over second number
                ("q1", "1"): ("q1", "1", "R"),
                # Found end — erase last 1
                ("q1", "_"): ("halt", "_", "L"),
            }

        elif name == "copy":
            # Copies a sequence of 1s
            # Example: 1 1 1 → 1 1 1 0 1 1 1
            self.tape = {0: "1", 1: "1", 2: "1"}
            self.head = 0
            self.state = "q0"
            self.rules = {
                ("q0", "1"): ("q1", "X", "R"),
                ("q0", "0"): ("q4", "0", "R"),
                ("q0", "_"): ("halt", "_", "R"),
                ("q1", "1"): ("q1", "1", "R"),
                ("q1", "0"): ("q2", "0", "R"),
                ("q1", "_"): ("q2", "_", "R"),
                ("q2", "1"): ("q2", "1", "R"),
                ("q2", "_"): ("q3", "1", "L"),
                ("q3", "1"): ("q3", "1", "L"),
                ("q3", "0"): ("q3", "0", "L"),
                ("q3", "X"): ("q0", "X", "R"),
                ("q4", "X"): ("q4", "1", "R"),
                ("q4", "_"): ("halt", "_", "R"),
            }

    def get_tape_view(self, window=20):
        # Return a slice of the tape centered on the head
        # for display purposes
        cells = []
        for i in range(self.head - window, self.head + window + 1):
            cells.append((i, self.tape.get(i, "_")))
        return cells