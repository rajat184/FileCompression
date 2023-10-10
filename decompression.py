import heapq
import pickle  # Used for loading Huffman codes

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

def load_huffman_codes(codes_file):
    with open(codes_file, 'rb') as f:
        huffman_codes = pickle.load(f)
    return huffman_codes

def decompress(input_file, output_file, huffman_codes):
    with open(input_file, 'rb') as f:
        data = f.read()

    padding_info = bin(data[0])[2:].rjust(8, '0')
    padding = int(padding_info, 2)

    encoded_text = ""
    for byte in data[1:]:
        encoded_text += bin(byte)[2:].rjust(8, '0')

    encoded_text = encoded_text[:-padding]

    decoded_text = ""
    current_code = ""
    for bit in encoded_text:
        current_code += bit
        if current_code in huffman_codes.values():
            char = [key for key, value in huffman_codes.items() if value == current_code][0]
            decoded_text += char
            current_code = ""

    with open(output_file, 'w') as f:
        f.write(decoded_text)

if __name__ == "__main__":
    input_file = "compressed.bin"
    output_file = "decompressed.txt"
    huffman_codes_file = "huffman_codes.pkl"

    huffman_codes = load_huffman_codes(huffman_codes_file)
    decompress(input_file, output_file, huffman_codes)
