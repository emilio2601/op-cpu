import struct

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

		opcode = self.memory[self.ip]

		if opcode == 0:
			"""
			hlt(register)
			Stop execution and exit with error code in register
			"""

			self.registers[0] = self.registers[self.memory[self.ip+1]] + 1
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
			self.registers[self.memory[self.ip+1]] = self.registers[self.memory[self.ip+1]] + 1
			self.ip += 2
			return

		if opcode == 4:
			self.registers[self.memory[self.ip+2]] = self.registers[self.memory[self.ip+1]]
			self.ip += 3
			return

		if opcode == 5:
			if(self.registers[self.memory[self.ip+1]] == self.registers[self.memory[self.ip+2]]):
				self.ip = self.memory[self.ip+3];
			else:
				self.ip += 4
			return
		
		raise Exception("Invalid opcode")

def big_endian_to_int(val):
	return struct.unpack(">Q", val)[0]