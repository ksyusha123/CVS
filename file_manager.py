from pathlib import Path
import zlib
from multiprocessing import Pool


def delete_directory(directory):
    for obj in directory.iterdir():
        if obj.is_dir():
            delete_directory(obj)
        else:
            obj.unlink()
    directory.rmdir()


def get_files(tree, old_commit_index, repository):
    with open(Path(repository.objects / tree)) as tree_file:
        for line in tree_file:
            obj_data = line.split()
            obj_type, obj_hash, name = obj_data[0], obj_data[1], obj_data[2]
            if obj_type == 'blob':
                old_commit_index.append(f"{name} {obj_hash}\n")
            else:
                get_files(obj_hash, old_commit_index, repository)


def update_index(repository, commit):
    old_commit_index = []
    with open(Path(repository.objects / commit)) as commit_obj:
        get_files(
            commit_obj.readline().split()[1], old_commit_index, repository)
    with open(repository.index, 'w') as index:
        index.writelines(old_commit_index)


def update_working_directory(repository):
    with open(repository.index) as index:
        for indexed_file in index:
            file_data = indexed_file.split()
            name, hash = file_data[0], file_data[1]
            old_file = Path(repository.objects / hash)
            current_file = Path(repository.path / name)
            current_file.write_bytes(_decompress_file(repository,
                                                           old_file))


def _decompress_file(repository, file):
    file_parts = _split_bytes_file(repository, file)
    with Pool() as pool:
        decompressed_file_parts = pool.map(_decompress_content,
                                           file_parts)
    return b''.join(decompressed_file_parts)


def _decompress_content(content):
    decompress_obj = zlib.decompressobj()
    decompressed_content = decompress_obj.decompress(content)
    return decompressed_content


def _split_bytes_file(repository, file):
    parts = []
    with open(Path(repository.path / file), 'rb') as f:
        content = f.read()
        split_content = content.split(b'--new-part--')
        parts += split_content
    return parts
