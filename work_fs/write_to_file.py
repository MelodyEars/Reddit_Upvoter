"""
write json
write line to file
add line to file
delete line in file by index
"""

import json


def write_json(filename, content=dict):
    """rewrite file"""
    with open(filename, "w") as f:  # a
        json.dump(content, f, indent=4)
        f.write('\n')
        f.close()


def write_list_to_file(filename, list_data):
    with open(filename, "w", encoding="utf8", errors="ignore") as file:
        for items in list_data:
            file.writelines(items + '\n')


def write_line(filename, list_line):
    """Writes line in file. Rewrite all info in the file."""
    with open(filename, "w+", encoding="utf8", errors="ignore") as file:
        if isinstance(list_line, list):
            list_line = (line for line in list_line if line.strip())

            file.seek(0)
            file.truncate()
            file.write("\n".join(str(line) for line in list_line))

        elif isinstance(list_line, str):
            file.seek(0)
            file.truncate()
            file.write(list_line + "\n")


def adder_list(filename, list_line):
    """ create file if not exists"""
    with open(filename, "a+", encoding="utf8", errors="ignore") as file:
        if list_line:
            if isinstance(list_line, list):
                list_line = [line for line in list_line if line.strip()]
                # list_line.sort()

                file.writelines(list_line)

            elif isinstance(list_line, str):
                file.write(list_line)
