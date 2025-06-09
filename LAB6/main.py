from keyboard import Keyboard


class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def show_menu():
    print(f"\n{Colors.BOLD}{Colors.OKCYAN}-- VIRTUAL KEYBOARD SIMULATOR --{Colors.ENDC}")
    print(f"{Colors.OKGREEN}Commands quick guide:{Colors.ENDC}")
    print(f"  Type any character to input text.")
    print(f"  Special combos (case-insensitive):")
    print(f"    {Colors.BOLD}ctrl+plus{Colors.ENDC}    - Volume Up")
    print(f"    {Colors.BOLD}ctrl+minus{Colors.ENDC}   - Volume Down")
    print(f"    {Colors.BOLD}ctrl+p{Colors.ENDC}       - Toggle Media Player")
    print(f"    {Colors.BOLD}ctrl+l{Colors.ENDC}       - Clear Screen")
    print(f"\n  Control commands:")
    print(f"    {Colors.BOLD}undo{Colors.ENDC}       - Undo last action")
    print(f"    {Colors.BOLD}redo{Colors.ENDC}       - Redo last undone action")
    print(f"    {Colors.BOLD}bindings{Colors.ENDC}   - Show all key bindings")
    print(f"    {Colors.BOLD}history{Colors.ENDC}    - Show command history")
    print(f"    {Colors.BOLD}stats{Colors.ENDC}      - Show keyboard stats")
    print(f"    {Colors.BOLD}clear{Colors.ENDC}      - Clear console output")
    print(f"    {Colors.BOLD}menu{Colors.ENDC}       - Show this menu")
    print(f"    {Colors.BOLD}exit{Colors.ENDC}       - Exit program")
    print(f"{Colors.OKCYAN}{'-'*30}{Colors.ENDC}")

def main():
    keyboard = Keyboard()
    print(f"{Colors.HEADER}Virtual Keyboard ready!{Colors.ENDC}")
    print(f"Your input and commands will appear here and be saved to 'output.txt'.\n")
    keyboard.output_manager.clear_file()
    show_menu()

    while True:
        try:
            user_input = input(f"{Colors.BOLD}{Colors.OKBLUE}Enter command > {Colors.ENDC}").strip()
            if not user_input:
                continue

            cmd = user_input.lower()
            if cmd == 'exit':
                print(f"{Colors.WARNING}Goodbye!{Colors.ENDC}")
                break
            elif cmd == 'undo':
                if keyboard.undo():
                    print(f"{Colors.OKGREEN}Undo successful.{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}Nothing to undo.{Colors.ENDC}")
            elif cmd == 'redo':
                if keyboard.redo():
                    print(f"{Colors.OKGREEN}Redo successful.{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}Nothing to redo.{Colors.ENDC}")
            elif cmd == 'bindings':
                print(f"{Colors.UNDERLINE}Current key bindings:{Colors.ENDC}")
                keyboard.show_bindings()
            elif cmd == 'history':
                print(f"{Colors.UNDERLINE}Command history:{Colors.ENDC}")
                keyboard.show_history()
            elif cmd == 'stats':
                stats = keyboard.get_stats()
                print(f"{Colors.OKCYAN}=== Keyboard Statistics ==={Colors.ENDC}")
                print(f" Total commands executed : {stats['total_commands']}")
                print(f" History current position: {stats['current_position']}")
                print(f" Defined key bindings    : {stats['key_bindings']}")
                print(f" Current text length     : {stats['current_text_length']}")
                print(f"{Colors.OKCYAN}{'='*26}{Colors.ENDC}")
            elif cmd == 'clear':
                keyboard.press_key('ctrl+l')
                print(f"{Colors.OKGREEN}Screen cleared.{Colors.ENDC}")
            elif cmd == 'menu':
                show_menu()
            elif user_input.startswith('bind '):
                parts = user_input.split(' ', 2)
                if len(parts) == 3:
                    _, key_combo, command_type = parts
                    keyboard.add_key_binding(key_combo, command_type)
                else:
                    print(f"{Colors.FAIL}Usage: bind <key_combination> <command_type>{Colors.ENDC}")
            elif user_input.startswith('unbind '):
                parts = user_input.split(' ', 1)
                if len(parts) == 2:
                    _, key_combo = parts
                    keyboard.remove_key_binding(key_combo)
                else:
                    print(f"{Colors.FAIL}Usage: unbind <key_combination>{Colors.ENDC}")
            else:
                if keyboard.press_key(user_input):
                    print(f"{Colors.OKGREEN}Command executed.{Colors.ENDC}")
                else:
                    print(f"{Colors.FAIL}Failed to execute command.{Colors.ENDC}")

        except KeyboardInterrupt:
            print(f"\n{Colors.WARNING}Interrupted by user. Goodbye!{Colors.ENDC}")
            break
        except Exception as e:
            print(f"{Colors.FAIL}Error: {e}{Colors.ENDC}")

if __name__ == "__main__":
    main()
