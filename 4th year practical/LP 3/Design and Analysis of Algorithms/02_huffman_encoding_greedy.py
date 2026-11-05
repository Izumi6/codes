"""
================================================================================
  Practical Assignment: Group A - Program 2
  Huffman Encoding using Greedy Strategy
  Course: Design and Analysis of Algorithms

  Problem Statement:
    Write a program to implement Huffman Encoding using a greedy strategy.
================================================================================
"""

import heapq
from collections import Counter


class Node:
    def __init__(self, char, freq):
        self.char = char
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq


def build_huffman_tree(text):
    freq_map = Counter(text)
    heap = [Node(ch, freq) for ch, freq in freq_map.items()]
    heapq.heapify(heap)

    if len(heap) == 1:
        root = Node(None, heap[0].freq)
        root.left = heap[0]
        return root, freq_map

    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)

        parent = Node(None, left.freq + right.freq)
        parent.left = left
        parent.right = right
        heapq.heappush(heap, parent)

    return heap[0], freq_map


def get_huffman_codes(root, code="", codes=None):
    if codes is None:
        codes = {}

    if root is None:
        return codes

    if root.char is not None:
        codes[root.char] = code if code else "0"
        return codes

    get_huffman_codes(root.left, code + "0", codes)
    get_huffman_codes(root.right, code + "1", codes)
    return codes


def decode_string(encoded_str, root):
    if not encoded_str or root is None:
        return ""

    decoded = []
    curr = root

    if curr.left is None and curr.right is None:
        return curr.char * len(encoded_str)

    for bit in encoded_str:
        curr = curr.left if bit == "0" else curr.right
        if curr.char is not None:
            decoded.append(curr.char)
            curr = root

    return "".join(decoded)


def main():
    print("--- Huffman Encoding using Greedy Strategy ---")
    text = input("Enter string: ").strip()
    if not text:
        print("Error: Input string cannot be empty.")
        return

    root, freq_map = build_huffman_tree(text)
    codes = get_huffman_codes(root)

    print("\nCharacter Frequencies:")
    for ch, freq in sorted(freq_map.items(), key=lambda x: x[1], reverse=True):
        print(f"  '{ch}' : {freq}")

    print("\nHuffman Codes:")
    for ch, code in sorted(codes.items()):
        print(f"  '{ch}' : {code}")

    encoded = "".join(codes[ch] for ch in text)
    decoded = decode_string(encoded, root)

    print(f"\nOriginal String : {text}")
    print(f"Encoded Bits    : {encoded}")
    print(f"Decoded String  : {decoded}")

    original_bits = len(text) * 8
    compressed_bits = len(encoded)
    saved = ((original_bits - compressed_bits) / original_bits) * 100

    print(f"\nOriginal Size (ASCII)  : {original_bits} bits")
    print(f"Compressed Size (Huffman): {compressed_bits} bits")
    print(f"Space Saved            : {saved:.2f}%")


if __name__ == "__main__":
    main()

"""
SAMPLE OUTPUT:
----------------------------------------------
--- Huffman Encoding using Greedy Strategy ---
Enter string: BCAADDDCCACACAC

Character Frequencies:
  'C' : 6
  'A' : 5
  'D' : 3
  'B' : 1

Huffman Codes:
  'A' : 11
  'B' : 100
  'C' : 0
  'D' : 101

Original String : BCAADDDCCACACAC
Encoded Bits    : 1000111110110110100110110110
Decoded String  : BCAADDDCCACACAC

Original Size (ASCII)  : 120 bits
Compressed Size (Huffman): 28 bits
Space Saved            : 76.67%
----------------------------------------------
"""
