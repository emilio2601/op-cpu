#include "stdio.h"
#include "string.h"
#include "stdlib.h"
#include "stdint.h"
#include "inttypes.h"
#include <sys/time.h>

uint64_t registers[255];
uint8_t* memory;
FILE *fp;

void copy_file_to_buffer(FILE *fp, uint8_t* buffer, size_t length){
	fseek(fp, 0, SEEK_END);
	uint64_t fsize = ftell(fp);
	rewind(fp);
	if(fsize < length){
		fread(buffer, fsize, 1, fp);
	}
	return;
}



uint8_t machine_loop(uint8_t* memory, uint64_t* registers){
	struct timeval tval_before, tval_after, tval_result;
	gettimeofday(&tval_before, NULL);
	uint64_t ip = 0;
	uint64_t exe = 0;
	while(1){
		exe = exe + 1;
		if(registers[0] != 0){
			gettimeofday(&tval_after, NULL);
			timersub(&tval_after, &tval_before, &tval_result);
			printf("time elapsed: %ld.%06ld instructions executed: %lld\n", (long int)tval_result.tv_sec, (long int)tval_result.tv_usec, exe);
			printf("exiting with error code: %" PRIu64 "\n", registers[0] - 1);
			return registers[0] - 1;
		} else {
		}


		uint8_t opcode = memory[ip];

		if(opcode == 0){ // hlt: exit with error code in next register
			registers[0] = registers[memory[ip+1]] + 1;

		} else if(opcode == 1){ // cpy: set 64 bit register with values
			uint8_t  in[8];
			uint64_t out;

			in[0] = memory[ip+9];
			in[1] = memory[ip+8];
			in[2] = memory[ip+7];
			in[3] = memory[ip+6];
			in[4] = memory[ip+5];
			in[5] = memory[ip+4];
			in[6] = memory[ip+3];
			in[7] = memory[ip+2];


			memcpy(&out, &in, 8);
			registers[memory[ip+1]] = out;
			ip = ip+10;

		} else if(opcode == 2){ //del: zero out register
			registers[memory[ip+1]] = 0;
			ip = ip + 2;

		} else if(opcode == 3){ //inc: increment
			registers[memory[ip+1]] = registers[memory[ip+1]] + 1;
			ip = ip + 2;

		} else if(opcode == 4){ //mov: copy register value to other register
			registers[memory[ip+2]] = registers[memory[ip+1]];
			ip = ip + 3;
			
		} else if(opcode == 5){ //jmp: jump if equal
			if(registers[memory[ip+1]] == registers[memory[ip+2]]){
				uint8_t  in[8];
				uint64_t out;

				in[0] = memory[ip+10];
				in[1] = memory[ip+9];
				in[2] = memory[ip+8];
				in[3] = memory[ip+7];
				in[4] = memory[ip+6];
				in[5] = memory[ip+5];
				in[6] = memory[ip+4];
				in[7] = memory[ip+3];

				memcpy(&out, &in, 8);
				ip = out;
			} else {
				ip = ip + 11;
			}
		}

		else {
			registers[0] = 255;
			exe++;
		}

	}
}

int main(int argc, char const *argv[])
{
	if(argc < 2){
		printf("input error: no file specified\n");
		return 1;
	} else if(argc > 2){
		printf("input error: too many arguments\n");
		return 1;
	}

	fp = fopen(argv[1], "r");
	if(fp == NULL){
		printf("input error: file %s does not exist or cannot be opened\n", argv[1]);
		return 1;
	}
	memory = calloc(1048576, 1);

	if(memory == NULL){
		printf("error: not enough memory\n");
		return 1;
	}

	copy_file_to_buffer(fp, memory, 1048576);

	uint8_t err = machine_loop(memory, registers);

	free(memory);
	fclose(fp);

	return err;
}

