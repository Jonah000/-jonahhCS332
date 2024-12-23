#Jonah Higgins
#jonahh
#HW2
#To compile: make
#To run: make run

# Compiler
CC = gcc

# Compiler flags
CFLAGS = -Wall -g

# Target executable
TARGET = traverse

# Source files
SRC = lab10.c

# Object files (generated from source files)
OBJ = $(SRC:.c=.o)


# Default rule to build the executable
$(TARGET): $(OBJ)
	$(CC) $(CFLAGS) -o $(TARGET) $(OBJ)

# Rule to compile .c files into .o files
%.o: %.c $(HEADERS)
	$(CC) $(CFLAGS) -c $< -o $@

# Clean up object files and the executable
clean:
	rm -f $(OBJ) $(TARGET)

# Convenience rule to run the program
run: $(TARGET)
	./$(TARGET)

# Phony targets
.PHONY: clean run