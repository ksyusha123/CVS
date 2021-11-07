from pathlib import Path
import zlib
import hashlib
from multiprocessing import Pool
from collections import deque
from os.path import relpath, getsize


def delete_directory(directory):
    for obj in directory.iterdir():
        if obj.is_dir():
            delete_directory(obj)
        else:
            obj.unlink()
    directory.rmdir()


def calculate_hash(repository, file):
    content_size = getsize(file)
    string_to_hash = f"blob {content_size}\\0"
    sha1 = hashlib.sha1(string_to_hash.encode())
    with open(Path(repository.path / file), 'rb') as f:
        while True:
            content = f.read()
            if not content:
                break
            sha1.update(content)
        file_hash = sha1.hexdigest()
    return file_hash


def bfs(root, get_children, get_values, must_be_in_answer, *args):
    answer = set()
    queue = deque()
    queue.append(root)
    while len(queue) != 0:
        current = queue.popleft()
        children = get_children(*args, current)
        values = get_values(*args, current)
        for value in values:
            if must_be_in_answer(*args, value):
                answer.add(value)
        for child in children:
            queue.append(child)
    return answer


def update_index(repository, commit):
    old_commit_index = []
    with open(Path(repository.objects / commit)) as commit_obj:
        get_files_from_commit_to_index(
            commit_obj.readline().split()[1], old_commit_index, repository)
    with open(repository.index, 'w') as index:
        index.writelines(old_commit_index)


def update_working_directory(repository):
    with open(repository.index) as index:
        for indexed_file in index:
            file_data = indexed_file.split()
            name, file_hash = file_data[0], file_data[1]
            old_file = Path(repository.objects / file_hash)
            current_file = Path(repository.path / name)
            current_file.write_bytes(_decompress_file(repository, old_file))


def compress_file(repository, file):
    file_parts = _split_file(repository, file)
    with Pool() as pool:
        compressed_file_parts = pool.map(_compress_content,
                                         file_parts)
    return b'--new-part--'.join(compressed_file_parts)


def get_subdirectories(repository, directory):
    subdirectories = set()
    for obj in directory.iterdir():
        if obj.is_dir() and obj != repository.cvs:
            subdirectories.add(obj)
    return subdirectories


def get_files_from_directory(repository, directory):
    files = set()
    for obj in directory.iterdir():
        if obj.is_file():
            files.add(relpath(obj, repository.path))
    return files


def get_files_from_commit_to_index(tree, old_commit_index, repository):
    with open(Path(repository.objects / tree)) as tree_file:
        for line in tree_file:
            obj_data = line.split()
            obj_type, obj_hash, name = obj_data[0], obj_data[1], obj_data[2]
            if obj_type == 'blob':
                old_commit_index.append(f"{name} {obj_hash}\n")
            else:
                get_files_from_commit_to_index(
                    obj_hash, old_commit_index, repository)


def is_untracked(repository, file):
    indexed_files = repository.indexed_files_info
    return file not in indexed_files


def is_tracked(repository, file):
    return not is_untracked(repository, file)


def get_commit_tree(repository, commit):
    with open(Path(repository.objects / commit)) as commit_obj:
        tree = commit_obj.readline().split()[1]
    return tree


def get_info_from_commit_tree(repository, tree):
    files_from_commit = bfs(tree, _get_subtrees, _get_blobs,
                            lambda *args: True, repository)
    return dict(files_from_commit)


def _get_subtrees(repository, tree):
    subtrees = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, file_hash, name = line.split()
            if filetype == 'tree':
                subtrees.add(file_hash)
    return subtrees


def _get_blobs(repository, tree):
    blobs = set()
    with open(Path(repository.objects / tree)) as tree_obj:
        for line in tree_obj:
            filetype, file_hash, name = line.split()
            if filetype == 'blob':
                blobs.add((name, file_hash))
    return blobs


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


def _compress_content(content):
    compress_obj = zlib.compressobj(level=9)
    compressed_content = compress_obj.compress(content)
    return compressed_content


def _split_file(repository, file):
    parts = []
    with open(Path(repository.path / file), 'rb') as f:
        while True:
            content = f.read(1048576)
            if not content:
                break
            parts.append(content)
    return parts
