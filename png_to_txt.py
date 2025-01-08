# Code authored by Anthony Albright
# albright.anthony21@gmail.com

import PNGify
import UniVerse
import loading
import traceback

DIRECTORY = "images"  # Directory to save and load PNG images

# -- Functions --

def png_to_txt(file_path):
    """Convert PNG to Unicode string."""
    try:
        rgb_reader = PNGify.PNGReader(file_path)  # Create a PNGReader instance for the specified file
        rgb_reader.read()  # Read the PNG file data
        rgb_tuples = rgb_reader.rgb_tuples  # Retrieve RGB tuples from the image
        header_pixel = rgb_tuples[0]  # Extract the header pixel which contains encoding info

        # Determine the encoding types based on the header pixel
        encoding_types = [None] * 3
        for i in range(3):
            encoding_types[i] = ['none', 'bin', 'uni'][header_pixel[i]]  # Extract encoding types
        rgb_data = rgb_tuples[1:]  # Extract RGB data excluding the header

        # Decode RGB data to Unicode string
        unicode_string = UniVerse.RGB.decode(rgb_data)

        # Apply additional decoding based on the encoding types in reverse order
        for encoding_type in reversed(encoding_types):
            if encoding_type == 'bin':
                unicode_string = UniVerse.Bin.decode(unicode_string)
            elif encoding_type == 'uni':
                unicode_string = UniVerse.Uni.decode(unicode_string)
            # 'none' does nothing

        return unicode_string  # Return the final decoded Unicode string

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")  # Error handling
        
        traceback_lines = traceback.format_exc().splitlines()
        print("Error occurred at line:", traceback_lines[-3].strip())
        return None  # Return None if an error occurred


def run_with_loading(file_path, file_name):
    """Run the png_to_txt function with a loading animation."""
    # Execute png_to_txt with a loading animation to inform the user
    result = loading.run(lambda: png_to_txt(file_path), message=f"Decoding {file_name}", interval=0.1, animation_type=loading.circle)
    return result  # Return the result of the decoding


# -- Main Program --

if __name__ == "__main__":
    print("This program allows the user to decode a PNG image to a Unicode string.")
    while True:
        # Prompt user for the name of the PNG file to decode
        file_name = input("\nInput the name of the PNG file you wish to decode (without the .png extension, leave empty to quit): ")
        if file_name == "":
            break  # Exit the loop if input is empty
        
        full_path = f"{DIRECTORY}/{file_name}.png"  # Construct the full path for the PNG file

        # Run decoding function with loading animation
        ret = png_to_txt(full_path)
        
        if ret is not None:
            print("Decoded Unicode String:")  # Display the decoded string
            print(ret)
        else:
            print("Failed to decode the image. Please check the file path and format.")  # Error message