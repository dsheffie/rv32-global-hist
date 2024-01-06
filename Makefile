OBJ = main.o functions.o
CXX = riscv32-unknown-elf-g++
CC = riscv32-unknown-elf-gcc
EXE = hist-len
OPT = -O2 -march=rv32im_zicsr
CXXFLAGS = -std=c++11 -g $(OPT)
DEP = $(OBJ:.o=.d)

.PHONY: all clean

all: $(EXE)

$(EXE) : $(OBJ)
	$(CXX) $(CXXFLAGS) $(OBJ) $(LIBS) -o $(EXE) -specs=htif.specs

%.o: %.cc
	$(CXX) -MMD $(CXXFLAGS) -c $<

%.o: %.s
	$(CC) -MMD -c $< 




-include $(DEP)

clean:
	rm -rf $(EXE) $(OBJ) $(DEP)
