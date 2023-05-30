import sys
import heapq
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QTextEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from graphviz import Digraph

# Fungsi untuk menghitung frekuensi kemunculan karakter
def count_frequency(text):
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1
    return frequency

# Fungsi untuk membangun pohon Huffman
def build_huffman_tree(frequency):
    heap = [[weight, [char, ""]] for char, weight in frequency.items()]
    heapq.heapify(heap)
    while len(heap) > 1:
        lo = heapq.heappop(heap)
        hi = heapq.heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heapq.heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heapq.heappop(heap)[1:], key=lambda p: (len(p[-1]), p))

# Fungsi untuk mengompresi teks
def compress_text(text, huffman_codes):
    compressed_text = ""
    for char in text:
        compressed_text += huffman_codes[char]
    return compressed_text

# Fungsi untuk menghitung persentase kompresi
def calculate_compression_ratio(original_size, compressed_size):
    ratio = (1 - (compressed_size / original_size)) * 100
    return ratio

# Fungsi untuk membuat gambar pohon Huffman
def create_huffman_tree_image(huffman_tree):
    dot = Digraph()
    for node in huffman_tree:
        char = node[0]
        code = node[1]
        dot.node(code, label=char)
        if len(node) > 2:
            for child in node[2:]:
                child_char = child[0]
                child_code = child[1]
                dot.node(child_code, label=child_char)
                dot.edge(code, child_code)
    dot.format = 'png'
    dot.render('huffman_tree', view=False)

# Fungsi untuk menampilkan GUI
class HuffmanCompressionGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Huffman Compression")
        self.setWindowIcon(QIcon("icon.png"))

        self.text_edit = QTextEdit()
        self.compress_button = QPushButton("Compress")
        self.compress_button.clicked.connect(self.compress)

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Input Text:"))
        layout.addWidget(self.text_edit)
        layout.addWidget(self.compress_button)

        self.setLayout(layout)
        self.show()

    def compress(self):
        text = self.text_edit.toPlainText()

        frequency = count_frequency(text)
        huffman_tree = build_huffman_tree(frequency)
        huffman_codes = {node[0]: node[1] for node in huffman_tree}

        compressed_text = compress_text(text, huffman_codes)
        original_size = len(text) * 8
        compressed_size = len(compressed_text)

        create_huffman_tree_image(huffman_tree)

        compression_ratio = calculate_compression_ratio(original_size, compressed_size)

        QMessageBox.information(self, "Compression Result", f"Compressed Text: {compressed_text}\n\n"
                                                            f"Original Size: {original_size} bits\n"
                                                            f"Compressed Size: {compressed_size} bits\n"
                                                            f"Compression Ratio: {compression_ratio:.2f}%")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = HuffmanCompressionGUI()
    sys.exit(app.exec_())
