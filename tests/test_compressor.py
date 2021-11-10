import unittest
from pathlib import Path

from compressor import Compressor


class TestCompressor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.file = Path('file')
        cls.compressed_file = Path('compressed')

    @classmethod
    def tearDownClass(cls):
        cls.file.unlink()
        cls.compressed_file.unlink()

    def test_decompress_small_file(self):
        with open(self.file, 'w') as f:
            f.write('small text')
        compressed_content = Compressor().compress_file(self.file)
        with open(self.compressed_file, 'wb') as compressed:
            compressed.write(compressed_content)
        decompressed_content = Compressor().decompress_file(
            self.compressed_file)
        assert 'small text' == decompressed_content.decode()

    def test_decompress_big_file(self):
        with open(self.file, 'w') as f:
            for _ in range(1000):
                f.write("abababababab")
        compressed_content = Compressor().compress_file(self.file)
        with open(self.compressed_file, 'wb') as compressed:
            compressed.write(compressed_content)
        decompressed_content = Compressor().decompress_file(
            self.compressed_file)
        with open(self.file, 'rb') as f:
            assert f.read() == decompressed_content
