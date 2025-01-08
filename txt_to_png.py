# Code authored by Anthony Albright
# albright.anthony21@gmail.com

import os
import PNGify
import UniVerse  
import loading

DIRECTORY = "images"
encoding_options = ['none', 'bin', 'uni']


def get_dimensions(n: int):
    """Calculate the height and width for the PNG image."""
    if n == 0:
        return 1, 1

    height = width = 1
    for i in range(1, int(n**0.5) + 1):
        if n % i == 0:
            height = i
            width = n // i

    return height, width

def header(encoding):
    """Create a header for encoding and decoding purposes."""
    try:
        r = encoding_options.index(encoding[0])
    except ValueError or IndexError:
        r = 0 
    try:
        g = encoding_options.index(encoding[1])
    except ValueError or IndexError:
        g = 0 
    try:
        b = encoding_options.index(encoding[2])
    except ValueError or IndexError:
        b = 0 
    return (r, g, b, 255)
    
def ex_encode(file_name, user_input):
    """Handles the header and encoding based on user input, allowing multiple encoding methods."""
    selected_encodings = ["none", "none", "none"]  # List to store selected encoding methods
    remaining_options = encoding_options.copy()  # Keep track of remaining encoding options

    # Check for encoding options in the file name
    for option in encoding_options:
        while option in file_name:
            user_choice = input(f"File name contains '{option}'. Use this encoding option? (y/n): ").strip().lower()
            if user_choice.startswith('y'):
                # Find the first available slot in selected_encodings to fill with this option
                for i in range(3):
                    if selected_encodings[i] == 'none':
                        selected_encodings[i] = option
                        break
                file_name = file_name.replace(option, "", 1)  # Remove one occurrence of the option
            else:
                break  # If user chooses not to use this encoding, stop asking for this option

    # Apply the selected encoding methods in sequence
    for encoding in selected_encodings:
        if encoding == 'bin':
            try:
                user_input = UniVerse.Bin.encode(user_input)
            except Exception as e:
                print(f"Error encoding input with 'bin': {e}")
                return None, selected_encodings
        elif encoding == 'uni':
            try:
                user_input = UniVerse.Uni.encode(user_input)
            except Exception as e:
                print(f"Error encoding input with 'uni': {e}")
                return None, selected_encodings

    return user_input, selected_encodings

def txt_to_png(txt, name, header_pixel):
    """Convert a text string to a PNG image."""
    rgb_list = UniVerse.RGB.encode(txt)
    rgb_list.insert(0, header_pixel)
    length = len(rgb_list)
    height, width = get_dimensions(length)

    png_creator = PNGify.PNGCreator(width, height, rgb_list)
    png_creator.save(name + ".png", DIRECTORY)

def inputs():
    """Get user input and file name."""
    user_input = input("\nPlease input a Unicode string (leave empty to quit): ")
    if not user_input:
        return None, None
    
    file_name = input("Enter the name for the PNG file (without file type): ").strip()
    
    if not file_name:
        print("Invalid file name. Please try again.")
        return None, None
    
    file_path = os.path.join(DIRECTORY, file_name + ".png")
    if os.path.exists(file_path):
        overwrite = input(f"File '{file_name}.png' exists. Overwrite? (y/n): ").strip().lower()
        if 'y' not in overwrite:
            print("Operation canceled.")
            return None, None

    return user_input, file_name

if __name__ == "__main__":
    print("This program converts a string into a PNG image.")
    print("To have extra encoding applied add the encoding type to your file name, refer to this list:")
    for option in encoding_options:
        if option != 'none':
            print(f"- {option}")

    
    while True:
        user_input, file_name = inputs()
        if user_input is None or file_name is None:
            break

        processed_input, encoding = ex_encode(file_name, user_input)
        if processed_input is None:
            continue  # 
        
        header_pixel = header(encoding)
        
        try:
            txt_to_png(processed_input, file_name, header_pixel)
            print(f"PNG file '{file_name}.png' created successfully!")
        except Exception as e:
            print(f"An error occurred: {e}")
