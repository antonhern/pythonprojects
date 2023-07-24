# steganography
import numpy as np
from matplotlib import image as mpimg
import matplotlib.pyplot as plt
from codec import Codec, CaesarCypher, HuffmanCodes
import cv2
from math import ceil

class Steganography():
    def __init__(self):
        self.text = ''
        self.binary = ''
        self.delimiter = '#'
        self.codec = None
        self.message = None

    def encode(self, filein, fileout, message, codec):
        image = cv2.imread(filein)
        self.message = message
        # calculate available bytes
        max_bytes = image.shape[0] * image.shape[1] * 3 // 8
        print("Maximum bytes available:", max_bytes)

        # convert into binary
        if codec == 'binary':
            self.codec = Codec()
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            self.codec = HuffmanCodes()

        # check if possible to encode the message
        # making my bin data equal to the message + delimiter
        bin_data = self.codec.encode(message + self.delimiter)
        num_bytes = ceil(len(bin_data) // 8) + 1
        if num_bytes > max_bytes:
            print("Error: Insufficient bytes!")
        else:
            print("Bytes to encode:", num_bytes)
        
        bit = 0
        self.text = message
        self.binary = bin_data

        # break up the r, g , b values inside the image
        # modify the image itself by changing the values.
        # a bit masking with a or 1 and then using and with 254
        for r in range(len(image)):
            for c in range(len(image[r])):
                for num in range(len(image[r][c])):
                    if bit < len(bin_data):
                        if bin_data[bit] == '1':
                            image[r][c][num] |= 1
                        else:
                            image[r][c][num] &= 254
                        bit += 1
        
        cv2.imwrite(fileout, image)

    def decode(self, filein, codec):
        image = cv2.imread(filein)

        # convert into text
        # checking every row, column, and the numbers inside of the image column
        # using a bit mask to get the least significant bit
        # then adding that bit/number to an empty string (as a string itself)
        # redefining self.text and self.binary

        flag = True
        if codec == 'binary':
            self.codec = Codec()
        elif codec == 'caesar':
            self.codec = CaesarCypher()
        elif codec == 'huffman':
            if self.codec is None or self.codec.name != 'huffman':
                print("A Huffman tree is not set!")
                flag = False
        
        if flag:
            binary_data = ""
            for row in image:
                for column in row:
                    for num in column:
                        bit = num & 1
                        binary_data += str(bit)
            
            self.text = self.codec.decode(binary_data)
            self.binary = self.codec.encode(self.message + self.delimiter)

    def print(self):
        if self.text == '':
            print("The message is not set.")
        else:
            print("Text message:", self.text)
            print("Binary message:", self.binary)

    def show(self, filename):
        plt.imshow(mpimg.imread(filename))
        plt.show()
