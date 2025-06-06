
def save(file, content):
    import os
    dir_path = os.path.dirname(file)
    if not os.path.isdir(dir_path):
        os.makedirs(dir_path)  # Create the directory if it doesn't exist
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)
        