from argparse import ArgumentParser, FileType
from CPU import CPU
import time
import sys


def main():
	parser = ArgumentParser(description="Interpreter for the register machine")
	parser.add_argument("infile", type=FileType("rb"), metavar="input", help="input file")
	args = parser.parse_args()

	cpu = CPU()

	cpu.load_file(args.infile)

	instr = 0
	start = time.time()
	while(not cpu.exit):
		cpu.next_instruction()
		instr += 1

	taken = time.time() - start
	ips = instr / taken

	print("Executed {} instructions in {:.4f} seconds".format(instr, taken))
	print("ips: {:.0f}".format(ips))


if __name__ == '__main__':
	main()