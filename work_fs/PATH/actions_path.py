from pathlib import Path


def move_file_or_dir(old_path: Path, new_path: Path):
	old_path.replace(new_path)

