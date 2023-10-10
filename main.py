import compression
import decompression

if __name__ == "__main__":
    # Compress
    input_text = "this is an example for huffman encoding"
    output_file = "compressed.bin"
    compression.compress(input_text, output_file)

    # Decompress
    input_file = "compressed.bin"
    output_file = "decompressed.txt"
    decompression.decompress(input_file, output_file)
