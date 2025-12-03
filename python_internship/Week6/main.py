
import time

# ----------- Decorator for logging runtime -----------
def log_runtime(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"Function '{func.__name__}' executed in {end - start:.4f} seconds")
        return result
    return wrapper

# ----------- Generator to read file line by line -----------
def read_file_generator(file_path):
    with open(file_path, 'r') as f:
        for line in f:
            yield line.strip()  # strip removes \n

# ----------- Context Manager for safe file handling -----------
class FileManager:
    def __init__(self, file_path, mode):
        self.file_path = file_path
        self.mode = mode
        self.file = None

    def __enter__(self):
        self.file = open(self.file_path, self.mode)
        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.file:
            self.file.close()
        # Do not suppress exceptions
        return False

# ----------- Processing pipeline with decorator -----------
@log_runtime
def process_file(file_path, keyword=None):
    count = 0
    # Using our generator to read file efficiently
    for line in read_file_generator(file_path):
        if keyword:
            if keyword.lower() in line.lower():
                print(line)
                count += 1
        else:
            count += 1
    print(f"Total lines processed: {count}")

# ----------- Example usage -----------
if __name__ == "__main__":
    # 1. Create a sample file safely using context manager
    sample_text = [
        "Hello World",
        "Python is awesome",
        "Generators are memory efficient",
        "Decorators are powerful",
        "Context managers help handle files safely",
        "Practice Python daily"
    ]
    with FileManager('sample.txt', 'w') as f:
        for line in sample_text:
            f.write(line + '\n')

    # 2. Process the file (all lines)
    print("\nProcessing all lines:")
    process_file('sample.txt')

    # 3. Process file filtering by keyword
    print("\nProcessing lines containing 'python':")
    process_file('sample.txt', keyword='python')
