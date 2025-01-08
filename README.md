# Text to PNG
This project serves to convert Unicode strings into PNG imaes.
To acomplish this each character is converted into there Unicode decimal point. This number is then used to choose a unique rgb value. Their also inculdes extra encoding methods that the user may select by adding their keywords to the file name. The full method for encoding is stored in the first rgb value and there for first pixel. It uses the r, b, and g values to store what extra encoding method was used, if any at all. After a list of rgb tuples is created it is conerted into a png image using the cusotm module PNGify where the program saves your text and a png image to a images directory.
Their is also a decoder included with the program wich esentially reverse the above methods of encoding. It collects the rgb tupple from the png selected, reads the header, and decodes the rgb tuples.


# Custom Modules
Their is also 3 custom modules contained with the project. PNGify, UniVerse, and loading.

**PNGify**
This handles the writing and reading of PNG's. Please view it's [repository](https://github.com/todo-jasny/PNGify) for more information on what it does and how it works.

**UniVerse**
UniVerse handles the encoding and decoding of its included methods. It has a class for each encoding method. They include subcasses to handel encoding and decoding seperatly.

**Loading**
Loading is a module to handle loading animation for the program.

# Instalation
1. Clone the repository
     ```bash
      git clone https://github.com/todo-jasny/Text-to-PNG.git

2. Move the project to your desired directory
3. Run the program
