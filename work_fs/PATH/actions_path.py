from pathlib import Path


def move_file_or_dir(old_path: Path, new_path: Path):
	old_path.replace(new_path)


def delete_dir(folder_path: Path):
	# check if the folder exists
	if folder_path.exists():

		# check if the folder is empty
		if not any(folder_path.glob('*')):
			# delete the folder
			folder_path.rmdir()
			print(f"{folder_path} has been deleted successfully.")

		else:
			# delete all the files and subfolders within the folder
			for sub in folder_path.glob('*'):
				if sub.is_file():
					sub.unlink()
				else:
					sub.rmdir()

			# delete the folder itself
			folder_path.rmdir()
			print(f"{folder_path} and all its contents have been deleted successfully.")

	else:
		print(f"{folder_path} does not exist.")
