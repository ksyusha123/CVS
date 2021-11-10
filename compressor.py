from multiprocessing import Pool
import zlib


class Compressor:

    def compress_file(self, filepath):
        file_parts = self._split_file(filepath)
        with Pool() as pool:
            compressed_file_parts = pool.map(self._compress_content,
                                             file_parts)
        return b'--new-part--'.join(compressed_file_parts)

    def decompress_file(self, filepath):
        file_parts = self._split_bytes_file(filepath)
        with Pool() as pool:
            decompressed_file_parts = pool.map(self._decompress_content,
                                               file_parts)
        return b''.join(decompressed_file_parts)

    @staticmethod
    def _decompress_content(content):
        decompress_obj = zlib.decompressobj()
        decompressed_content = decompress_obj.decompress(content)
        return decompressed_content

    @staticmethod
    def _split_bytes_file(filepath):
        parts = []
        with open(filepath, 'rb') as f:
            content = f.read()
            split_content = content.split(b'--new-part--')
            parts += split_content
        return parts

    @staticmethod
    def _compress_content(content):
        compress_obj = zlib.compressobj(level=9)
        compressed_content = compress_obj.compress(content)
        compressed_content += compress_obj.flush()
        return compressed_content

    @staticmethod
    def _split_file(filepath):
        parts = []
        with open(filepath, 'rb') as f:
            while True:
                content = f.read(1048576)
                if not content:
                    break
                parts.append(content)
        return parts
