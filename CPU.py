import struct
import sys

class CPU():
	def __init__(self, memory=1048576):
		self.memory = bytearray(memory)
		self.ip = 0
		self.exit = False
		self.registers = []
		for i in range(255):
			self.registers.append(0)


	def load_file(self, file):
		for index, byte in enumerate(file.read()):
			self.memory[index] = byte

	def next_instruction(self):
		if self.registers[0] != 0:
			self.exit = True
			self.err = self.registers[0]

		opcode = self.memory[self.ip]

		if opcode == 0:
			"""
			hlt(register)
			Stop execution and exit with error code in register
			"""

			self.registers[0] = self.registers[self.memory[self.ip+1]]
			return

		if opcode == 1:
			"""
			cpy(register, int)
			Copy 64 bit integer to register
			"""
			val = big_endian_to_int(self.memory[self.ip+2:self.ip+10])
			self.registers[self.memory[self.ip+1]] = val
			self.ip += 10
			return

		if opcode == 2:
			"""
			del(register)
			Zero out register
			"""
			self.registers[self.memory[self.ip+1]] = 0
			self.ip += 2
			return

		if opcode == 3:
			"""
			inc(register)
			Increment value on register by one
			"""
			self.registers[self.memory[self.ip+1]] = self.registers[self.memory[self.ip+1]] + 1
			self.ip += 2
			return

		if opcode == 4:
			"""
			mov(register, register)
			Moves value in first register to second register
			"""
			self.registers[self.memory[self.ip+2]] = self.registers[self.memory[self.ip+1]]
			self.ip += 3
			return

		if opcode == 5:
			"""
			jmp(register, register, int)
			If the values in the first two registers are equal, jump to address in third operand
			"""
			if(self.registers[self.memory[self.ip+1]] == self.registers[self.memory[self.ip+2]]):
				self.ip = big_endian_to_int(self.memory[self.ip+3:self.ip+11])
			else:
				self.ip += 11
			return

		if opcode == 6:
			"""
			outb(register, int)
			Outputs int number of bytes from register, starting from the LSB
			"""
			n = big_endian_to_int(self.memory[self.ip+2:self.ip+10])
			sys.stdout.write(int_to_big_endian(self.registers[self.memory[self.ip+1]])[-n:].decode("utf-8"))
			self.ip += 10
			return

		if opcode == 7:
			"""
			outn(register)
			Outputs the value of register as a base 10 number
			"""
			sys.stdout.write(str(self.registers[self.memory[self.ip+1]]))
			self.ip += 2
			return

		raise Exception("Invalid opcode")

def big_endian_to_int(val):
	return struct.unpack(">Q", val)[0]

def int_to_big_endian(val):
	return struct.pack(">Q", val)