import random


class Chip8:
    def __init__(self):
        # 4096 bytes of memory
        self.memory = [0] * 4096
        # 16 general purpose registers V0-VF
        self.v = [0] * 16
        # Index register
        self.i = 0
        # Program counter — programs start at 0x200
        self.pc = 0x200
        # Stack for subroutine calls
        self.stack = []
        # Delay and sound timers
        self.delay_timer = 0
        self.sound_timer = 0
        # 64x32 pixel display
        self.display = [[0] * 64 for _ in range(32)]
        # Keypad state — 16 keys
        self.keys = [False] * 16
        # Draw flag — tells screen to redraw
        self.draw_flag = False
        self.running = False
        self.steps = 0

        # Load fontset into memory starting at 0x000
        self.load_fontset()

    def load_fontset(self):
        fontset = [
            0xF0, 0x90, 0x90, 0x90, 0xF0,  # 0
            0x20, 0x60, 0x20, 0x20, 0x70,  # 1
            0xF0, 0x10, 0xF0, 0x80, 0xF0,  # 2
            0xF0, 0x10, 0xF0, 0x10, 0xF0,  # 3
            0x90, 0x90, 0xF0, 0x10, 0x10,  # 4
            0xF0, 0x80, 0xF0, 0x10, 0xF0,  # 5
            0xF0, 0x80, 0xF0, 0x90, 0xF0,  # 6
            0xF0, 0x10, 0x20, 0x40, 0x40,  # 7
            0xF0, 0x90, 0xF0, 0x90, 0xF0,  # 8
            0xF0, 0x90, 0xF0, 0x10, 0xF0,  # 9
            0xF0, 0x90, 0xF0, 0x90, 0x90,  # A
            0xE0, 0x90, 0xE0, 0x90, 0xE0,  # B
            0xF0, 0x80, 0x80, 0x80, 0xF0,  # C
            0xE0, 0x90, 0x90, 0x90, 0xE0,  # D
            0xF0, 0x80, 0xF0, 0x80, 0xF0,  # E
            0xF0, 0x80, 0xF0, 0x80, 0x80,  # F
        ]
        for i, byte in enumerate(fontset):
            self.memory[i] = byte

    def reset(self):
        self.memory = [0] * 4096
        self.v = [0] * 16
        self.i = 0
        self.pc = 0x200
        self.stack = []
        self.delay_timer = 0
        self.sound_timer = 0
        self.display = [[0] * 64 for _ in range(32)]
        self.keys = [False] * 16
        self.draw_flag = False
        self.running = False
        self.steps = 0
        self.load_fontset()

    def load_rom(self, rom_bytes):
        # Load ROM into memory starting at 0x200
        self.reset()
        for i, byte in enumerate(rom_bytes):
            if 0x200 + i < 4096:
                self.memory[0x200 + i] = byte
        self.running = True

    def step(self):
        if not self.running:
            return

        # Fetch — read 2 bytes and combine into one 16-bit opcode
        opcode = (self.memory[self.pc] << 8) | self.memory[self.pc + 1]
        self.pc += 2
        self.steps += 1

        # Decode and execute
        self.execute(opcode)

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            self.sound_timer -= 1

    def execute(self, opcode):
        # Extract common nibbles
        nnn = opcode & 0x0FFF       # 12-bit address
        n   = opcode & 0x000F       # 4-bit nibble
        x   = (opcode >> 8) & 0xF  # Register x
        y   = (opcode >> 4) & 0xF  # Register y
        kk  = opcode & 0x00FF       # 8-bit byte

        # Decode by first nibble
        first = (opcode >> 12) & 0xF

        if opcode == 0x00E0:
            # Clear display
            self.display = [[0] * 64 for _ in range(32)]
            self.draw_flag = True

        elif opcode == 0x00EE:
            # Return from subroutine
            self.pc = self.stack.pop()

        elif first == 0x1:
            # Jump to address nnn
            self.pc = nnn

        elif first == 0x2:
            # Call subroutine at nnn
            self.stack.append(self.pc)
            self.pc = nnn

        elif first == 0x3:
            # Skip if Vx == kk
            if self.v[x] == kk:
                self.pc += 2

        elif first == 0x4:
            # Skip if Vx != kk
            if self.v[x] != kk:
                self.pc += 2

        elif first == 0x5:
            # Skip if Vx == Vy
            if self.v[x] == self.v[y]:
                self.pc += 2

        elif first == 0x6:
            # Set Vx = kk
            self.v[x] = kk

        elif first == 0x7:
            # Set Vx = Vx + kk
            self.v[x] = (self.v[x] + kk) & 0xFF

        elif first == 0x8:
            if n == 0x0:
                self.v[x] = self.v[y]
            elif n == 0x1:
                self.v[x] |= self.v[y]
            elif n == 0x2:
                self.v[x] &= self.v[y]
            elif n == 0x3:
                self.v[x] ^= self.v[y]
            elif n == 0x4:
                result = self.v[x] + self.v[y]
                self.v[0xF] = 1 if result > 255 else 0
                self.v[x] = result & 0xFF
            elif n == 0x5:
                self.v[0xF] = 1 if self.v[x] > self.v[y] else 0
                self.v[x] = (self.v[x] - self.v[y]) & 0xFF
            elif n == 0x6:
                self.v[0xF] = self.v[x] & 0x1
                self.v[x] >>= 1
            elif n == 0x7:
                self.v[0xF] = 1 if self.v[y] > self.v[x] else 0
                self.v[x] = (self.v[y] - self.v[x]) & 0xFF
            elif n == 0xE:
                self.v[0xF] = (self.v[x] >> 7) & 0x1
                self.v[x] = (self.v[x] << 1) & 0xFF

        elif first == 0x9:
            # Skip if Vx != Vy
            if self.v[x] != self.v[y]:
                self.pc += 2

        elif first == 0xA:
            # Set I = nnn
            self.i = nnn

        elif first == 0xB:
            # Jump to nnn + V0
            self.pc = nnn + self.v[0]

        elif first == 0xC:
            # Set Vx = random byte AND kk
            self.v[x] = random.randint(0, 255) & kk

        elif first == 0xD:
            # Draw sprite at (Vx, Vy) with height n
            vx = self.v[x] % 64
            vy = self.v[y] % 32
            self.v[0xF] = 0

            for row in range(n):
                sprite_byte = self.memory[self.i + row]
                for col in range(8):
                    if sprite_byte & (0x80 >> col):
                        px = (vx + col) % 64
                        py = (vy + row) % 32
                        if self.display[py][px]:
                            self.v[0xF] = 1
                        self.display[py][px] ^= 1
            self.draw_flag = True

        elif first == 0xE:
            if kk == 0x9E:
                # Skip if key Vx is pressed
                if self.keys[self.v[x] & 0xF]:
                    self.pc += 2
            elif kk == 0xA1:
                # Skip if key Vx is not pressed
                if not self.keys[self.v[x] & 0xF]:
                    self.pc += 2

        elif first == 0xF:
            if kk == 0x07:
                self.v[x] = self.delay_timer
            elif kk == 0x0A:
                # Wait for key press
                for k in range(16):
                    if self.keys[k]:
                        self.v[x] = k
                        return
                self.pc -= 2
            elif kk == 0x15:
                self.delay_timer = self.v[x]
            elif kk == 0x18:
                self.sound_timer = self.v[x]
            elif kk == 0x1E:
                self.i = (self.i + self.v[x]) & 0xFFFF
            elif kk == 0x29:
                self.i = (self.v[x] & 0xF) * 5
            elif kk == 0x33:
                self.memory[self.i] = self.v[x] // 100
                self.memory[self.i + 1] = (self.v[x] // 10) % 10
                self.memory[self.i + 2] = self.v[x] % 10
            elif kk == 0x55:
                for reg in range(x + 1):
                    self.memory[self.i + reg] = self.v[reg]
            elif kk == 0x65:
                for reg in range(x + 1):
                    self.v[reg] = self.memory[self.i + reg]