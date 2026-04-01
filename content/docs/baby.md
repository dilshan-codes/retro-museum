# Manchester Baby

## What Is It?
The Manchester Baby, officially named the Small-Scale Experimental Machine 
(SSEM), was built at the University of Manchester in 1948. It was the first 
computer in history to store both its program and data in electronic memory 
and execute that program. Every computer today works on this same principle.

## Who Built It?
Freddie Williams and Tom Kilburn built the Baby with the help of engineer 
Geoff Tootill. They were testing a new type of memory called the Williams 
Tube — a cathode ray tube that could store binary data as dots on a screen.

## The First Program Ever Run
On June 21, 1948, the Baby ran its first program written by Tom Kilburn. 
The program found the highest factor of a number by trying every possible 
divisor. It took 52 minutes and 3.5 million operations to find the answer. 
This was the first time a computer had ever run a stored program in history.

## How Does It Work?
The Baby had:
- 32 memory locations each storing a 32-bit number
- One accumulator register for calculations
- A program counter that tracked which instruction to run next
- Only 7 instructions it could execute

## The 7 Instructions
| Instruction | What It Does |
|---|---|
| JMP | Jump to address stored in memory |
| JRP | Jump relative using value in memory |
| LDN | Load negative of memory value into accumulator |
| STO | Store accumulator value into memory |
| SUB | Subtract memory value from accumulator |
| CMP | Skip next instruction if accumulator is negative |
| STP | Stop the program |

## Why Does It Matter?
Before the Baby, computers were programmed by physically rewiring them for 
each new task. The Baby proved that a program could live in memory alongside 
data and be changed instantly without touching any hardware. This idea — the 
stored program concept — is the foundation of every computer built since 1948.

## Using The Emulator
- The memory grid shows all 32 memory locations as binary values
- Press Step to execute one instruction and watch memory and registers update
- The current instruction is decoded and shown in plain English below
- Press Run to execute the preloaded first-ever program automatically
- Watch the accumulator and program counter change with each step