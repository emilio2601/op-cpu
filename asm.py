import struct

class Instruction(object):
		def __init__(self, text):
			self.label = None
			self.instruction = None
			self.width = 0
			self.location = 0
			self.bytecode = ""

			text = text.split(" ")
			self.text = text
			first = text[0]

			if first[0] == ":":
				self.label = first[1:]
			else:
				self.instruction = first

			if self.instruction:
				if self.instruction == "hlt":
					self.width = 2
				elif self.instruction == "cpy":
					self.width = 10
				elif self.instruction == "del":
					self.width = 2
				elif self.instruction == "inc":
					self.width = 2
				elif self.instruction == "mov":
					self.width = 3
				elif self.instruction == "jmp":
					self.width = 4
			
		def __repr__(self):
			if self.label: 		return "<Label {}>".format(self.label)
			if self.instruction: return "<Instruction {} bytecode={}>".format(self.instruction, self.bytecode)

		def parse(self, table):
			if self.label:
				return
			else:
				if self.instruction == "hlt":
					opcode = 0
					reg = self.str_to_reg(self.text[1])
					self.bytecode = struct.pack("BB", opcode, reg)

				elif self.instruction == "cpy":
					opcode = 1
					reg = self.str_to_reg(self.text[1])
					try:
						val = int(self.text[2])
					except ValueError:
						raise Exception("Invalid input")
					self.bytecode = struct.pack("BB", opcode, reg)
					self.bytecode += struct.pack(">Q", val)

				elif self.instruction == "del":
					opcode = 2
					reg = self.str_to_reg(self.text[1])
					self.bytecode = struct.pack("BB", opcode, reg)

				elif self.instruction == "inc":
					opcode = 3
					reg = self.str_to_reg(self.text[1])
					self.bytecode = struct.pack("BB", opcode, reg)

				elif self.instruction == "mov":
					opcode = 4
					reg_src = self.str_to_reg(self.text[1])
					reg_dst = self.str_to_reg(self.text[2])
					self.bytecode = struct.pack("BBB", opcode, reg_src, reg_dst)
					
				elif self.instruction == "jmp":
					opcode = 5
					reg_one = self.str_to_reg(self.text[1])
					reg_two = self.str_to_reg(self.text[2])
					label = self.text[3]
					addr = 0
					for lookup_label in table:
						if lookup_label[0] == label:
							addr = lookup_label[1]
					self.bytecode = struct.pack("BBBB", opcode, reg_one, reg_two, addr)

		def str_to_reg(self, string):
			if not string.startswith("r"):
				raise Exception("Invalid input")
			string = string[1:]
			try:
				reg = int(string)
			except ValueError:
				raise Exception("Invalid input")
			if 0 <= reg <= 255:
				return reg
			else:
				raise Exception("Invalid input")


		def set_location(self, location):
			self.location = location