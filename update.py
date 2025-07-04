import os
import hashlib
import json

def get_file_hash(filepath):
    """Compute SHA-256 hash of a file."""
    with open(filepath, 'rb') as f:
        return hashlib.sha256(f.read()).hexdigest()

def iterate_dir(path):
    """Recursively iterate through a directory and return structured JSON-like dict."""
    result = {"isdir": True, "childs": {}}
    for entry in os.scandir(path):
        if entry.name in (".", ".."):
            continue
        full_path = os.path.join(path, entry.name)
        if entry.is_file():
            file_info = {
                "isdir": False,
                "sha256": get_file_hash(full_path),
                "url": f"https://gamepiaynmo.github.io/GPKWebsite/{full_path.replace(os.sep, '/')}"
            }
            result["childs"][entry.name] = file_info
        elif entry.is_dir():
            result["childs"][entry.name] = iterate_dir(full_path)
    return result

def main():
    version_path = os.path.join("Files", "version.txt")

    # Read version
    with open(version_path, 'r') as f:
        version = int(f.read().strip())

    # Increment and write version
    with open(version_path, 'w') as f:
        f.write(str(version + 1))

    # Traverse directory and generate JSON structure
    json_data = iterate_dir("Files")

    # Write JSON to update.json
    with open("update.json", 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)

if __name__ == "__main__":
    main()
