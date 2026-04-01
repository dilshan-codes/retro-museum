# CHIP-8

## What Is It?
CHIP-8 is a simple programming language and virtual machine created in 1977 
by Joseph Weisbecker at RCA. It was designed to make game development easier 
on early hobbyist computers. Instead of writing complex machine code, 
programmers could write CHIP-8 programs that ran on any computer with a 
CHIP-8 interpreter installed.

## Why Does It Matter?
CHIP-8 is one of the earliest examples of a virtual machine — a program that 
pretends to be a computer. This is the same idea behind Java, Android, and 
every modern app platform. Weisbecker invented this concept for hobbyists 
in 1977, decades before it became mainstream.

## The Hardware It Ran On
CHIP-8 was originally designed for the COSMAC VIP and Telmac 1800 computers. 
These were hobbyist kit computers sold in the late 1970s. Owners would 
assemble them from parts and program them directly in machine code — until 
CHIP-8 made programming accessible to everyday hobbyists.

## Technical Specifications
| Component | Specification |
|---|---|
| Memory | 4096 bytes total |
| Registers | 16 general purpose (V0 to VF) |
| Display | 64 x 32 pixels, black and white |
| Stack | 16 levels deep |
| Keypad | 16 keys (0 to F) |
| Timers | Delay timer and sound timer |
| Instructions | 35 opcodes |

## How Does It Work?
The CHIP-8 CPU follows a simple cycle on every tick:
1. Fetch the next 2-byte instruction from memory
2. Decode what the instruction means
3. Execute the instruction
4. Move to the next instruction

This fetch-decode-execute cycle is the same cycle used by every CPU ever 
built, from the Manchester Baby to the chip inside your phone today.

## Famous Games
CHIP-8 became popular because people wrote classic games for it including 
Pong, Space Invaders, Tetris, and Pac-Man. These games are tiny programs 
that fit inside a few hundred bytes of memory yet are fully playable.

## Using The Emulator
- Press Load ROM to load a CHIP-8 program file
- The 64x32 display updates in real time as the program runs
- Watch the 16 registers update live in the register panel
- Use the speed slider to run faster or slower
- The on-screen keypad maps to CHIP-8s 16 hex keys
- Press Step to execute one instruction at a time
- Press Pause to freeze execution at any point