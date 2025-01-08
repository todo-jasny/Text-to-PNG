import struct
import zlib
import os

# -- PNG Creator Class --

class PNGCreator:
    """A class for creating PNG images from RGBA pixel data."""

    def __init__(self, width, height, pixel_colors):
        """Initialize the PNGCreator with width, height, and pixel colors."""
        self.width = width
        self.height = height
        self.pixel_colors = pixel_colors
        self.png_signature = b'\x89PNG\r\n\x1a\n'  # PNG file signature

    def create_chunk(self, chunk_type, data):
        """Create a single PNG chunk with the given type and data."""
        chunk = struct.pack('>I', len(data)) + chunk_type + data  # Pack chunk length and type
        crc = zlib.crc32(chunk_type + data) & 0xffffffff  # Calculate CRC for the chunk
        chunk += struct.pack('>I', crc)  # Append the CRC to the chunk
        return chunk

    def create_ihdr_chunk(self):
        """Create the IHDR chunk, which contains image header information."""
        ihdr_data = struct.pack('>IIBBBBB', self.width, self.height, 8, 6, 0, 0, 0)  # Image header data for RGBA
        return self.create_chunk(b'IHDR', ihdr_data)  # Return the IHDR chunk

    def create_idat_chunk(self):
        """Create the IDAT chunk, which contains the compressed image data."""
        image_data = self.create_image_data()  # Create raw image data
        compressed_data = zlib.compress(image_data)  # Compress the image data
        return self.create_chunk(b'IDAT', compressed_data)  # Return the IDAT chunk

    def create_iend_chunk(self):
        """Create the IEND chunk, which marks the end of the PNG file."""
        return self.create_chunk(b'IEND', b'')  # Return the IEND chunk

    def create_image_data(self):
        """Create the raw image data for the PNG from RGBA pixel colors."""
        row = bytearray()  # Initialize bytearray for image data
        for y in range(self.height):
            row.append(0)  # Add filter byte (0 = no filter)
            for x in range(self.width):
                # Get the RGBA values for the current pixel
                r, g, b, a = self.pixel_colors[y * self.width + x]

                # Append R, G, B, A values to the row
                row.extend([r, g, b, a])

        return row  # Return the complete image data

    def save(self, file_name, directory=None):
        """Save the PNG file to the specified directory."""
        ihdr_chunk = self.create_ihdr_chunk()  # Create IHDR chunk
        idat_chunk = self.create_idat_chunk()  # Create IDAT chunk
        iend_chunk = self.create_iend_chunk()  # Create IEND chunk

        # Construct the complete PNG data
        png_data = self.png_signature + ihdr_chunk + idat_chunk + iend_chunk

        # Ensure the directory exists
        if directory:
            os.makedirs(directory, exist_ok=True)  # Create directory if it does not exist
            file_path = os.path.join(directory, file_name)  # Construct full file path
        else:
            file_path = file_name  # Use provided file name directly

        # Write the PNG data to a file
        with open(file_path, 'wb') as f:
            f.write(png_data)  # Save PNG data to the specified file


# -- PNG Reader Class --

class PNGReader:
    """A class for reading PNG images and extracting RGBA pixel data."""

    def __init__(self, file_path):
        """Initialize the PNGReader with the path to the PNG file."""
        self.file_path = file_path
        self.width = 0
        self.height = 0
        self.rgb_tuples = []

    def read(self):
        """Read the PNG file and extract pixel data."""
        def read_chunk(f):
            """Read a chunk from the PNG file."""
            chunk_length = struct.unpack('>I', f.read(4))[0]
            chunk_type = f.read(4)
            chunk_data = f.read(chunk_length)
            f.read(4)  # Read and discard CRC
            return chunk_type, chunk_data

        with open(self.file_path, 'rb') as f:
            # Read and validate PNG signature
            signature = f.read(8)
            if signature != b'\x89PNG\r\n\x1a\n':
                raise ValueError("Not a valid PNG file.")

            compressed_data = b""
            palette = []

            while True:
                chunk_type, chunk_data = read_chunk(f)

                if chunk_type == b'IHDR':
                    # Parse the IHDR chunk
                    self.width, self.height, _, self.color_type, *_ = struct.unpack('>IIBBBBB', chunk_data)
                    print(self.color_type)
                elif chunk_type == b'PLTE':
                    # Parse the PLTE chunk for Indexed-color mode
                    palette = [
                        (chunk_data[i], chunk_data[i + 1], chunk_data[i + 2])
                        for i in range(0, len(chunk_data), 3)
                    ]
                elif chunk_type == b'IDAT':
                    # Accumulate IDAT chunks
                    compressed_data += chunk_data
                elif chunk_type == b'IEND':
                    break

            # Decompress IDAT chunk data and extract pixel data
            decompressed_data = zlib.decompress(compressed_data)
            self.rgb_tuples = self.extract_pixel_data(decompressed_data, palette)

    def extract_pixel_data(self, decompressed_data, palette):
        """Extract pixel data and convert to RGBA if needed."""
        pixels = []
        index = 0

        for y in range(self.height):
            filter_type = decompressed_data[index]
            index += 1  # Skip filter byte
            for x in range(self.width):
                if self.color_type == 0:  # Grayscale
                    gray = decompressed_data[index]
                    # Convert grayscale to RGBA (gray, gray, gray, 255)
                    pixels.append((gray, gray, gray, 255))
                    index += 1
                elif self.color_type == 2:  # Truecolor (RGB)
                    r, g, b = decompressed_data[index:index+3]
                    # Convert RGB to RGBA (r, g, b, 255)
                    pixels.append((r, g, b, 255))
                    index += 3
                elif self.color_type == 3:  # Indexed-color
                    palette_index = decompressed_data[index]
                    r, g, b = palette[palette_index]
                    # Convert indexed color to RGBA (r, g, b, 255)
                    pixels.append((r, g, b, 255))
                    index += 1
                elif self.color_type == 4:  # Grayscale with Alpha
                    gray, alpha = decompressed_data[index:index+2]
                    # Convert grayscale with alpha to RGBA (gray, gray, gray, alpha)
                    pixels.append((gray, gray, gray, alpha))
                    index += 2
                elif self.color_type == 6:  # Truecolor with Alpha
                    r, g, b, alpha = decompressed_data[index:index+4]
                    pixels.append((r, g, b, alpha))
                    index += 4
                else:
                    raise ValueError(f"Unsupported color type: {self.color_type}")

        return pixels

def resize_png(file_path, new_width, new_height):
    """Resize the PNG to the specified new width and height."""
    reader = PNGReader(file_path)
    reader.read()
    rgba_tuples = reader.rgb_tuples
    old_height = reader.height
    old_width = reader.width

    # Create a list to store the resized RGBA pixel data
    new_rgba_tuples = []

    for i in range(new_height):
        for j in range(new_width):
            # Map the new dimensions to the original image's pixels
            orig_x = (j * old_width) // new_width
            orig_y = (i * old_height) // new_height
            
            # Get the pixel color from the original image
            pixel_color = rgba_tuples[orig_y * old_width + orig_x]
            new_rgba_tuples.append(pixel_color)

    # Create a new PNG image with the specified new dimensions and pixel data
    creator = PNGCreator(new_width, new_height, new_rgba_tuples)
    output_file = os.path.splitext(file_path)[0] + f"_{new_width}x{new_height}.png"
    creator.save(output_file)