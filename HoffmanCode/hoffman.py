import heapq
from collections import Counter
from bitstring import BitArray
from pathlib import Path

# for tests
import string
import random
def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

TEST_SIZES= [0,
             1,
             1000,
             ]

def test():
    for size in TEST_SIZES:
        for i in range(size + 1):
            string = id_generator(size)
            if not HuffmanCode().encode(string).decode() == string:
                print("LossLess compression Test Failed!")
                print("String: ", string)
                return

class HuffmanCode:
    def __init__(self, text=None):
        self.text = text
        if text is not None:
            self.encode(text)

    def compress(self, source, target):
        with Path(source).open(mode='rb') as f, Path(target, mode='wb') as g:
            self.encode(f.read())
            self.bits.tofile(g)
            self.comp_size = g.stat().st_size
            self.orig_size = f.stat().st_size
            self.comp_rate = self.orig_size / self.comp_size

    def save(self, target):
        with Path(target).open(mode='wb') as f:
            if self.bits:
                self.bits.tofile(f)

    def encode(self, text):
        tree, encoding_dict = build_huffman_tree(*_get_freq(text))
        code_dict = {}
        bits = BitArray()
        for c in text:
            bits.append(_get_code(c, code_dict, encoding_dict))
        self.bits = bits
        self.length = len(text)
        self.tree = tree
        return self

    def decode(self):
        bits, length, root = self.bits, self.length, self.tree
        res = ""
        res_len = 0
        node = root
        for bit in bits:
            if res_len < length:
                if node._is_leaf():
                    res += node.c
                    node = root
                    res_len +=1
                if bit:
                    node = node.right
                else:
                    node = node.left
        else:
            if node._is_leaf():
                res += node.c
                node = root
                res_len +=1
        return res

def _get_code(chr, code_dict, encoding_dict):
    code = code_dict.get(chr)
    if code is None:
        leaf = encoding_dict[chr]
        code = leaf._root_path()
        code_dict[chr] = code
    return code


def _get_freq(string):
    n = len(string)
    counts = Counter(string)
    freqs = {}
    total_chars = 0
    for k,v in counts.items():
        freqs[k] = v / n
        total_chars += 1
    return freqs, total_chars


def build_huffman_tree(frequencies, total_chars):
    if total_chars == 0:
        node = Node(weight=1,chr='')
        encoding_dict = {'': node}
        return node, encoding_dict

    heap = []
    encoding_dict = {}
    for k,v in frequencies.items():
        leaf = Node(weight=v, chr=k)
        encoding_dict[k] = leaf
        heapq.heappush(heap, leaf)

    while heap:
        left = heapq.heappop(heap)
        if heap:
            right = heapq.heappop(heap)
            node = Node(weight=left.w + right.w, left=left, right=right)
            right.p = node
            left.p = node
            heapq.heappush(heap, node)
        else:
            root = left
            root.p = root
            return root, encoding_dict


class Node:
    def __init__(self, weight=0, chr=None, left=None, right=None, parent=None):
        self.w = weight
        self.c = chr
        self.p = parent
        self.left = left
        self.right = right

    def __eq__(self, value):
        return self.w == value.w

    def __lt__(self, value):
        return self.w <= value.w

    def __str__(self):
        return "Weight: " + str(self.w) + ", Char: " + str(self.c)

    def _is_leaf(self):
        return self.left is None and self.right is None

    def _root_path(self):
        code = BitArray()
        node = self
        while not node._is_root():
            if node._is_left_child():
                code.prepend('0b0')
            else:
                code.prepend('0b1')
            node = node.p
        return code

    def _is_root(self):
        return self.p is self

    def _is_left_child(self):
        return self.p.left is self
