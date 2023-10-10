import heapq
import os

class HuffmanNode:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    priority_queue = [HuffmanNode(char, freq) for char, freq in frequency.items()]
    heapq.heapify(priority_queue)

    while len(priority_queue) > 1:
        left = heapq.heappop(priority_queue)
        right = heapq.heappop(priority_queue)

        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left = left
        merged.right = right

        heapq.heappush(priority_queue, merged)

    return priority_queue[0]

def build_huffman_codes(node, current_code="", huffman_codes={}):
    if node is None:
        return

    if node.char is not None:
        huffman_codes[node.char] = current_code
        return

    build_huffman_codes(node.left, current_code + "0", huffman_codes)
    build_huffman_codes(node.right, current_code + "1", huffman_codes)

def compress(text, output_file):
    root = build_huffman_tree(text)
    huffman_codes = {}
    build_huffman_codes(root, "", huffman_codes)

    encoded_text = "".join([huffman_codes[char] for char in text])
    padding = 8 - len(encoded_text) % 8
    encoded_text += padding * "0"  # Add padding to make the length a multiple of 8
    padding_info = "{0:08b}".format(padding)

    encoded_bytes = bytearray()
    for i in range(0, len(encoded_text), 8):
        byte = encoded_text[i:i + 8]
        encoded_bytes.append(int(byte, 2))

    with open(output_file, 'wb') as f:
        f.write(bytes([int(padding_info, 2)]) + bytes(encoded_bytes))

if __name__ == "__main__":
    input_text = "this is an example for huffman encoding"
    output_file = "compressed.bin"
    compress(input_text, output_file)
