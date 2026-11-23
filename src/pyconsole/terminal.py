import os
import subprocess
import sys


def main():
    print("=== Simple Python Terminal ===")
    print("Type commands as you would in Linux. Type 'exit' to quit.\n")

    while True:
        try:
            # Show the current directory in the prompt.
            current_dir = os.getcwd()
            # prompt input
            command = input(f"py-term{current_dir}%")
        except KeyboardInterrupt, EOFError:
            print("\nExiting Terminal...")
            break

        # Strip whitespace
        command = command.strip()

        # Skip empty lines
        if not command:
            continue

        # Handle exit command
        if command == "exit":
            print("Goodbye!")
            break

        # Handle 'cd' (change directory) specially because it changes state
        # inside the Python proces rather than a separate subprocess.
        if command.startswith("cd "):
            path = command[3:]
            # Handle home directory expansion (~/)
            if path.startswith("~"):
                path = os.path.expanduser(path)
            try:
                os.chdir(path)
            except FileNotFoundError:
                print(f"cd: no suchfile or directory: {path}")
            except NotADirectoryError:
                print(f"cd: not a directory: {path}")
            except PermissionError:
                print(f"cd: permission denied: {path}")
            except Exception as e:
                print(f"cd error: {e}")

            continue

        # Execute all other commands using subprocess
        try:
            # shell=True allows piping, redirection, and standard Linux commands.
            result = subprocess.run(command, shell=True, capture_output=True, text=True)

            # Print standard output if any
            if result.stdout:
                print(result.stdout, end="")

            # Print standard error if any
            if result.stderr:
                print(result.stderr, end="", file=sys.stderr)

        except Exception as e:
            print(f"Error executing command: {e}")


if __name__ == "__main__":
    main()
