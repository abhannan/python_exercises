import os, pprint, hashlib, sys

duplicate_list = []

def get_hash(file_name):
	hash_md5 = hashlib.md5()
	with open(file_name, 'rb') as file:
		for chunk in iter(lambda: file.read(4096), b""):
			hash_md5.update(chunk)
	return hash_md5.hexdigest()

def check_for_duplicates(paths):
	hashes = {}
	for path in paths:
		for root, dirs, files in os.walk(path):
			for file in files:
				absolute_path = os.path.join(os.path.abspath(root), file)
				file_size = os.path.getsize(absolute_path)
				file_hash = get_hash(absolute_path)
				file_id = (file_hash, file_size)
				duplicate = hashes.get(file_id, None)
				if duplicate:
					duplicate_list.append([absolute_path, duplicate])
				else:
					hashes[file_id] = absolute_path
	pprint.pprint(duplicate_list)

if sys.argv[1:]:
    check_for_duplicates(sys.argv[1:])
else:
    print("Please provide the directory to find duplicate files")
