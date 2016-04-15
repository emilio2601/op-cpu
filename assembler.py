from argparse import ArgumentParser, FileType
import sys
import struct
from asm import Instruction


def main():
	parser = ArgumentParser(description="Assembler for the register machine")
	parser.add_argument("infile", type=FileType("r"), metavar="input", help="input file")
	parser.add_argument("outfile", type=FileType("wb"), metavar="output", help="output file")
	args = parser.parse_args()
	input_p = [' '.join(line.split()) for line in args.infile]
	output = []
	
	for line in input_p:
		if line == "":
			pass
		else:
			output.append(Instruction(line))

	loc = 0
	for instr in output:
		instr.set_location(loc)
		loc += instr.width

	table = []
	for instr in output:
		if instr.instruction: pass
		else:
			table.append((instr.label, instr.location))
	
	for instr in output:
		instr.parse(table)

	out = b""

	for instr in output:
		if instr.instruction: out += instr.bytecode

	args.outfile.write(out)



if __name__ == '__main__':
	main()