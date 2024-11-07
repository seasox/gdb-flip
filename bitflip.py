import gdb

# Global variable to collect output messages
output_messages = []

class BitFlipCommand(gdb.Command):
    """Flip a specified bit in a variable within a specified function at a specified line.

    Usage:
        bitflip <file> <line> <variable_name> <bit_position>
    """

    def __init__(self):
        super(BitFlipCommand, self).__init__("bitflip", gdb.COMMAND_USER)
        self.current_breakpoint = None

    def invoke(self, args, from_tty):
        args = gdb.string_to_argv(args)
        
        if len(args) != 4:
            output_messages.append("Usage: bitflip <file> <line> <variable_name> <bit_position>")
            return

        file_name, line, variable_name, bit_position = args[0], int(args[1]), args[2], int(args[3])

        # Clear any previous breakpoint
        if self.current_breakpoint:
            gdb.execute(f"delete {self.current_breakpoint.number}")
            self.current_breakpoint = None

        # Set a new breakpoint at the specified file and line
        breakpoint_location = f"{file_name}:{line}"
        self.current_breakpoint = gdb.Breakpoint(breakpoint_location)
        self.current_breakpoint.silent = True
        self.variable_name = variable_name
        self.bit_position = bit_position
        output_messages.append(f"Breakpoint set at '{breakpoint_location}' to flip bit {bit_position} of '{variable_name}'")

        # Hook stop to handle the breakpoint
        gdb.events.stop.connect(self.flip_bit_on_stop)

    def flip_bit_on_stop(self, event):
        # Check if the event is a breakpoint and that it matches our set breakpoint
        if isinstance(event, gdb.BreakpointEvent) and self.current_breakpoint in event.breakpoints:
            frame = gdb.selected_frame()

            try:
                # Try to access the variable
                var_info = frame.read_var(self.variable_name)
                var_type = var_info.type
                byte_position = self.bit_position // 8
                if var_type.code == gdb.TYPE_CODE_ARRAY:
                    # Handle array variables by accessing the first element for bit flipping
                    # Assuming the array is of a standard type like char, int, etc.
                    element_type = var_type.target()
                    element_value = var_info[byte_position]  # find byte position
                else:
                    element_value = var_info  # Single variable
                
                new_value = int(element_value) ^ (1 << self.bit_position % 8)
                
                # Set the variable to the new value
                # Set the variable to the new value, respecting whether it's an array or a single variable
                if var_type.code == gdb.TYPE_CODE_ARRAY:
                    gdb.execute(f"set var {self.variable_name}[{byte_position}] = {new_value}")  # Change first element
                    output_messages.append(f"Flipped bit {self.bit_position} in byte {byte_position} of '{self.variable_name}'; new value: {new_value}")
                else:
                    gdb.execute(f"set var {self.variable_name} = {new_value}")
                    output_messages.append(f"Flipped bit {self.bit_position} in '{self.variable_name}'; new value: {new_value}")
            except ValueError as e:
                output_messages.append(f"Error: Unable to access variable '{self.variable_name}' - {e}")
            except gdb.error as e:
                output_messages.append(f"GDB Error: {e}")

            # Continue program execution
            gdb.execute("continue")

# Register the bitflip command with GDB
BitFlipCommand()


class BitFlipWrapper(gdb.Command):
    """Wrapper to start a program, set bitflip at a line, and continue execution.
    
    Usage:
        bitflip_wrapper <program> <file> <line> <variable_name> <bit_position>
    """

    def __init__(self):
        super(BitFlipWrapper, self).__init__("bitflip_wrapper", gdb.COMMAND_USER)

    def invoke(self, args, from_tty):
        args = gdb.string_to_argv(args)

        if len(args) < 5:
            output_messages.append("Usage: bitflip_wrapper <program> <file> <line> <variable_name> <bit_position>")
            return

        program, file_name, line, variable_name, bit_position = args[0], args[1], int(args[2]), args[3], int(args[4])

        # Load the program
        gdb.execute(f"file {program}")

        # Use the bitflip command with a specific line in the file
        gdb.execute(f"bitflip {file_name} {line} {variable_name} {bit_position}")

        # Start the program execution
        gdb.execute("run", to_string=True)

        # Print collected output messages after the run
        for message in output_messages:
            print(message)

# Register the wrapper command with GDB
BitFlipWrapper()

