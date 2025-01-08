# Code authored by Anthony Albright
# albright.anthony21@gmail.com

"""
UniVerse is a powerful encoding and decoding Python module designed for transforming Unicode strings 
into various formats. It supports multiple methods for encoding and decoding, enabling flexible and 
dynamic text manipulation. With its intuitive interface, UniVerse allows users to seamlessly convert 
Unicode text into distinct representations, paving the way for innovative applications in data 
processing and visualization.
"""

import hashlib
import math

# -- Uni Class for Unicode Encoding and Decoding --

class Uni:
    """A class to encode and decode strings to and from Unicode code points (decimal representation)."""
    
    @staticmethod
    def encode(text):
        """Convert a string of Unicode characters to a string of decimal Unicode code points."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        # Convert each character to its decimal Unicode code point
        return ' '.join(format(ord(char)) for char in text)

    @staticmethod
    def decode(unicode_point):
        """Convert a string of space-separated decimal Unicode code points back to a Unicode string."""
        if not isinstance(unicode_point, str):
            raise ValueError("Input must be a string of decimal Unicode code points.")
        # Convert each decimal code point back to the corresponding character
        return ''.join(chr(int(point)) for point in unicode_point.split())

# -- Bin Class for Binary Representation Encoding and Decoding --

class Bin:
    """A class to encode and decode strings to and from binary representation."""
    
    @staticmethod
    def encode(text):
        """Convert a string of Unicode characters to a binary string."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")
        # Convert each character to its binary representation (8 bits)
        return ' '.join(format(ord(char), '08b') for char in text)

    @staticmethod
    def decode(binary_string):
        """Convert a binary string back to a Unicode string."""
        if not isinstance(binary_string, str):
            raise ValueError("Input must be a binary string.")
        # Convert each binary string back to the corresponding character
        return ''.join(chr(int(binary, 2)) for binary in binary_string.split())

# -- RGB Class for RGB Tuple Encoding and Decoding --

class RGB:
    """A class to encode and decode strings to and from RGB tuples."""
    
    @staticmethod
    def encode(text):
        """Convert a string of Unicode characters to a list of RGB tuples with unique mappings."""
        if not isinstance(text, str):
            raise ValueError("Input must be a string.")

        def unicode_to_rgb(char):
            """Convert a single Unicode character to an RGB tuple based on a hash of the Unicode value."""
            a = 255

            if char == ' ':
                return (0, 0, 0, a)  # Force ' ' to always be (0, 0, 0)
            
            unicode_val = ord(char)  # Get the Unicode value of the character
            hash_object = hashlib.md5(str(unicode_val).encode())  # Create a hash of the Unicode value
            hash_hex = hash_object.hexdigest()  # Get the hexadecimal representation of the hash
            r = int(hash_hex[:2], 16)  # Extract red component
            g = int(hash_hex[2:4], 16)  # Extract green component
            b = int(hash_hex[4:6], 16)  # Extract blue component
            return r, g, b, a  # Return the RGB tuple

        # Convert each character in the text to its corresponding RGB tuple
        return [unicode_to_rgb(char) for char in text]

    @staticmethod
    def decode(rgb_list):
        """Convert a list of RGB tuples back to a string of Unicode characters."""
        if not isinstance(rgb_list, list) or not all(isinstance(item, tuple) and len(item) == 3 for item in rgb_list):
            raise ValueError("Input must be a list of RGB tuples.")

        def rgb_to_unicode(rgb):
            """Find the Unicode character that corresponds to the given RGB tuple."""
            a = 255

            if rgb == (0, 0, 0, a):
                return ' '  # Return space for (0, 0, 0)
            
            r, g, b, a = rgb  # Unpack RGB values
            # Iterate over potential Unicode values to find the matching character
            for unicode_val in range(32, 0x110000):  # Start from 32 to skip control characters
                hash_object = hashlib.md5(str(unicode_val).encode())
                hash_hex = hash_object.hexdigest()
                char_rgb = (
                    int(hash_hex[:2], 16),
                    int(hash_hex[2:4], 16),
                    int(hash_hex[4:6], 16)
                )
                if char_rgb == (r, g, b):
                    return chr(unicode_val)  # Return the matching character

            return '?'  # Placeholder if no match found

        # Convert each RGB tuple back to its corresponding Unicode character
        return ''.join(rgb_to_unicode(rgb) for rgb in rgb_list)
