with open('large_file.txt', 'w') as f:
    for i in range(50000000):
        f.write('a')
