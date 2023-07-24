# codecs
class Codec():
    def __init__(self):
        self.name = 'binary'
        self.delimiter = '00100011'  # a hash symbol '#'

    # convert text or numbers into binary form
    def encode(self, text):
        if type(text) == str:
            return ''.join([format(ord(i), "08b") for i in text])
        else:
            print('Format error')

    # convert binary data into text
    def decode(self, data):
        binary = []
        for i in range(0, len(data), 8):
            byte = data[i: i + 8]
            if byte == self.delimiter:
                break
            binary.append(byte)
        text = ''
        for byte in binary:
            text += chr(int(byte, 2))
        return text


class CaesarCypher(Codec):
    def __init__(self, shift=3):
        self.name = 'caesar'
        self.delimiter = '#'  # you may need to set up it to a corresponding binary code
        self.shift = shift
        self.chars = 256  # total number of characters

    # convert text into binary form
    def encode(self, text):
        data = ''
        values = []
        bin_vals = []
        if type(text) == str:
            data = [chr((ord(i) + self.shift) % 256) for i in text]
            return ''.join([format(ord(i), "08b") for i in data])
        else:
            print('Format Error')

    # convert binary data into text
    def decode(self, data):
        self.delimiter = '00100110'
        new_bin = []
        for i in range(0, len(data), 8):
            byte = data[i: i + 8]
            if byte == self.delimiter:
                break
            new_bin.append(byte)
        text = ''
        for byte in new_bin:
            x = int(byte, 2) - self.shift
            z = x % 256
            text += chr(z)
            if x < 0:
                y = x + 256
                text += chr(y)
        return text


# a helper class used for class HuffmanCodes that implements a Huffman tree
class Node:
    def __init__(self, freq, symbol, left=None, right=None):
        self.left = left
        self.right = right
        self.freq = freq
        self.symbol = symbol
        self.code = ''


class HuffmanCodes(Codec):
    def __init__(self):
        self.nodes = None
        self.name = 'huffman'

    # make a Huffman Tree
    def make_tree(self, data):
        # make nodes
        nodes = []
        for char, freq in data.items():
            nodes.append(Node(freq, char))
        # assemble the nodes into a tree
        while len(nodes) > 1:
            # sort the current nodes by frequency
            nodes = sorted(nodes, key=lambda x: x.freq)
            # pick two nodes with the lowest frequencies
            left = nodes[0]
            right = nodes[1]
            # assign codes
            left.code = '0'
            right.code = '1'
            # combine the nodes into a tree
            root = Node(left.freq + right.freq, left.symbol + right.symbol, left, right)
            # remove the two nodes and add their parent to the list of nodes
            nodes.remove(left)
            nodes.remove(right)
            nodes.append(root)
        return nodes

    # traverse a Huffman tree
    def traverse_tree(self, node, val, enc):
        next_val = val + node.code
        if node.left:
            self.traverse_tree(node.left, next_val, enc)
        if node.right:
            self.traverse_tree(node.right, next_val, enc)
        if not node.left and not node.right:
            enc[node.symbol] = next_val

    # convert text into binary form
    def encode(self, text):
        data = ""
        freq = dict()
        # making an empty dictionary and adding to it the frequencies in which letters appear inside a string
        # then making the nodes equal to the first key every time after that I make a new dictionary
        # in this new one, I add the traversed tree values and make those the new data string
        for letter in text:
            freq.setdefault(letter, 0)
            freq[letter] += 1
        self.nodes = self.make_tree(freq)[0]
        enc = dict()
        self.traverse_tree(self.nodes, '', enc)
        for letter in text:
            data += enc[letter]
        return data

    # convert binary data into text
    def decode(self, data):
        self.delimiter = '#'
        text = ""
        curr = self.nodes
        for i in range(len(data)):
            if data[i] == "0":
                curr = curr.left
            if data[i] == "1":
                curr = curr.right
            if curr.symbol == self.delimiter:
                break
            if curr.left is None and curr.right is None:
                text += curr.symbol
                curr = self.nodes
        return text


# driver program for codec classes
if __name__ == '__main__':
    text = 'hello#'
    print('Original:', text)
    c = Codec()
    binary = c.encode(text)
    print('Binary:', binary)
    data = c.decode(binary)
    print('Text:', data)
    cc = CaesarCypher()
    binary = cc.encode(text)
    print('Binary:', binary)
    data = cc.decode(binary)
    print('Text:', data)
    h = HuffmanCodes()
    binary = h.encode(text)
    print('Binary:', binary)
    data = h.decode(binary)
    print('Text:', data)
