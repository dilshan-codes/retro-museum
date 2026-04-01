class Navigator:

    def __init__(self):
        self.stack = ["home"]
        self.pointer = 0

    def go_to(self, route):
        self.stack = self.stack[:self.pointer + 1]
        self.stack.append(route)
        self.pointer += 1

    def current(self):
        return self.stack[self.pointer]

    def back(self):
        if self.pointer > 0:
            self.pointer -= 1
        return self.stack[self.pointer]

    def forward(self):
        if self.pointer < len(self.stack) - 1:
            self.pointer += 1
        return self.stack[self.pointer]
    
    