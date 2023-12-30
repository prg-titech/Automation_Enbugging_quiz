import os

def get_dir_size(path='.'):
    total = 0
    with os.scandir(path) as it:
        for entry in it:
            if entry.is_file():
                total += entry.stat().st_size
    return total

original_size = get_dir_size('./error_sample_place')
print(original_size/100)
small_size = get_dir_size('./error_sample_small_place')
print(small_size/100)

print((small_size/100)/(original_size/100))