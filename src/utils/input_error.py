# Customized exception class to handle and print invalid user inputs for both utilities

class InputError(Exception):
    def handle_input_error(e):
        print(f'{e.__class__.__name__}: {e}')
