class ManchesterBaby:
    def __init__(self):
        # 32 words of 32-bit memory
        self.memory = [0] * 32
        # Accumulator register
        self.accumulator = 0
        # Program counter
        self.pc = 0
        self.running = False
        self.steps = 0
        self.current_instruction = ""

    def reset(self):
        self.memory = [0] * 32
        self.accumulator = 0
        self.pc = 0
        self.running = False
        self.steps = 0
        self.current_instruction = ""

    def load_first_program(self):
        # Load the actual first program ever run — June 21 1948
        # Written by Tom Kilburn to find the highest factor of a number
        # This is a simplified version that finds highest factor of 18
        self.reset()

        # Store the number to factorize at address 24
        self.memory[24] = 18
        # Store -1 at address 25 for comparison
        self.memory[25] = -1

        # The program — stored in memory starting at address 0
        # Each instruction: bits 0-4 = line number, bits 13-15 = opcode
        # We encode as (line, opcode) tuples for readability
        # Opcodes: 0=JMP, 1=JRP, 2=LDN, 3=STO, 4=SUB, 6=CMP, 7=STP

        # Simplified program that counts down and demonstrates the machine
        self.memory[0] = self.encode(24, 2)   # LDN 24 — load negative of mem[24]
        self.memory[1] = self.encode(25, 4)   # SUB 25 — subtract mem[25] (-1), so add 1
        self.memory[2] = self.encode(26, 3)   # STO 26 — store result
        self.memory[3] = self.encode(26, 2)   # LDN 26 — load negative back
        self.memory[4] = self.encode(6, 6)    # CMP    — skip next if accumulator negative
        self.memory[5] = self.encode(0, 7)    # STP    — stop
        self.memory[6] = self.encode(0, 0)    # JMP 0  — jump back to start

        self.pc = 0
        self.running = True

    def encode(self, line, opcode):
        # Baby stores instructions with line in bits 0-4, opcode in bits 13-15
        return (opcode << 13) | (line & 0x1F)

    def decode(self, word):
        # Extract line number and opcode from instruction word
        line = word & 0x1F
        opcode = (word >> 13) & 0x7
        return line, opcode

    def step(self):
        if not self.running:
            return False

        # Fetch instruction from memory at program counter
        instruction = self.memory[self.pc % 32]
        line, opcode = self.decode(instruction)

        # Decode opcode names for display
        opcode_names = {
            0: "JMP", 1: "JRP", 2: "LDN",
            3: "STO", 4: "SUB", 6: "CMP", 7: "STP"
        }
        name = opcode_names.get(opcode, "???")
        self.current_instruction = f"{name} {line}  (PC={self.pc})"

        # Execute instruction
        if opcode == 0:   # JMP — jump to address in memory[line]
            self.pc = self.memory[line % 32]
        elif opcode == 1: # JRP — jump relative
            self.pc += self.memory[line % 32]
        elif opcode == 2: # LDN — load negative
            self.accumulator = -self.memory[line % 32]
        elif opcode == 3: # STO — store accumulator
            self.memory[line % 32] = self.accumulator
        elif opcode == 4: # SUB — subtract
            self.accumulator -= self.memory[line % 32]
        elif opcode == 6: # CMP — skip if accumulator negative
            if self.accumulator < 0:
                self.pc += 1
        elif opcode == 7: # STP — stop
            self.running = False
            self.current_instruction = "STP — Machine stopped"
            self.steps += 1
            return False

        # Increment program counter
        self.pc = (self.pc + 1) % 32
        self.steps += 1
        return True

    def to_binary(self, value, bits=32):
        # Convert integer to binary string for display
        if value < 0:
            # Two's complement for negative numbers
            value = value & ((1 << bits) - 1)
        return format(value, f'0{bits}b')

    def get_memory_display(self):
        # Return memory as list of binary strings for display
        return [self.to_binary(word) for word in self.memory]