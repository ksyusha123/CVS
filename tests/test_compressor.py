import unittest
from pathlib import Path

from compressor import Compressor


class TestCompressor(unittest.TestCase):

    def test_decompress_small_file(self):
        file = Path('file')
        with open(file, 'w') as f:
            f.write('small text')
        compressed_content = Compressor().compress_file(file)
        compressed_file = Path('compressed')
        with open(compressed_file, 'wb') as compressed:
            compressed.write(compressed_content)
        decompressed_content = Compressor().decompress_file(compressed_file)
        assert 'small text' == decompressed_content.decode()
        file.unlink()
        compressed_file.unlink()

    # def test_decompress_big_file(self):
