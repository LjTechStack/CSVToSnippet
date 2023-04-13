"""Module to use csv parser."""
import csv
import json
import os.path
import plistlib
import sys
import uuid

from model.OutputType import OutputType

TAB_DELIMITER = "\t"
NAME = "name"
KEYWORD = "keyword"
SNIPPET = "snippet"
FOLDER_JSON = "folder_json"
FOLDER_PLIST = "folder_plist"
SNIPPET_KEYWORD_PREFIX = "snippetkeywordprefix"
SNIPPET_KEYWORD_SUFFIX = "snippetkeywordsuffix"


def parse_header_data(header: list[str], output_type: OutputType) -> dict[str, int]:
    """Parse the header row of a CSV file"""
    header_map = {}
    for index, ele in enumerate(header):
        if "folder" == ele:
            if output_type == OutputType.JSON:
                header_map[FOLDER_JSON] = index
            else:
                header_map[FOLDER_PLIST] = index
        else:
            header_map[ele] = index
    return header_map


def snippet_maker(snippet_name: str, snippet_keyword: str, snippet: str, unique_id: str) -> dict:
    """Create an Alfred snippet from the given parameters"""
    snippet_dict = {"snippet": "" + snippet,
                    "uid": unique_id,
                    "name": snippet_name,
                    "keyword": snippet_keyword}
    return {"alfredsnippet": snippet_dict}


def plist_maker(snippetkeywordprefix: str, snippetkeywordsuffix: str) -> dict:
    """Create a plist dictionary from the given parameters"""
    plist_dict = {
        "snippetkeywordprefix": snippetkeywordprefix, "snippetkeywordsuffix": snippetkeywordsuffix
    }
    return plist_dict


def remove_existing_file(base_file_path: str, file_sub_string: str):
    """Removed existing file with other uniqueID pattern"""
    for filename in os.listdir(base_file_path):
        if file_sub_string + "[" in filename:
            os.remove(base_file_path + "/" + filename)


def make_directory_if_not_created(path: str):
    """Create directory if yet created"""
    if not os.path.isdir(path):
        os.mkdir(path)


def generate_base_path(folder: str) -> str:
    """Get base path for folder"""
    root_path = "output"
    make_directory_if_not_created(root_path)
    snippet_path = "output/snippets"
    make_directory_if_not_created(snippet_path)
    base_path = snippet_path + "/" + folder
    make_directory_if_not_created(base_path)
    return base_path


def process_csv_data(line_data: list[str], header_map: dict[str, int], output_type: OutputType):
    """Process the csv data"""
    folder = line_data[header_map[FOLDER_JSON]].strip() \
        if output_type == OutputType.JSON else line_data[header_map[FOLDER_PLIST]].strip()
    base_path = generate_base_path(folder)

    if output_type == OutputType.PLIST:
        snippet_keyword_prefix = line_data[header_map[SNIPPET_KEYWORD_PREFIX]].strip()
        snippet_keyword_suffix = line_data[header_map[SNIPPET_KEYWORD_SUFFIX]].strip()
        with open(base_path + "/info.plist", "wb") as outfile:
            plistlib.dump(plist_maker(snippet_keyword_prefix, snippet_keyword_suffix), outfile)
    elif output_type == OutputType.JSON:
        name = line_data[header_map[NAME]].strip()
        snippet_keyword = line_data[header_map[KEYWORD]].strip()
        snippet = line_data[header_map[SNIPPET]].strip()
        unique_id = uuid.uuid4()
        remove_existing_file(base_path, name)
        with open(base_path + '/' + name + '[' + str(unique_id) + "].json", "w",
                  encoding="utf8") as outfile:
            json.dump(snippet_maker(name, snippet_keyword, snippet, str(unique_id)), outfile)


def read_csv_file(root: str, csv_file_name: str, output_type: OutputType):
    """Read content of csv file"""
    with open(os.path.join(root, csv_file_name)) as csv_file:
        csvreader = csv.reader(csv_file, delimiter=TAB_DELIMITER)
        header_map = parse_header_data(next(csvreader), output_type)
        for line in csv.reader(csv_file, delimiter=TAB_DELIMITER):
            process_csv_data(line, header_map, output_type)


def process_input_dir(input_dir: str):
    """Loop thought input directory"""
    for (root, path, files) in os.walk(input_dir):
        for file in files:
            if 'snippet.csv' in file:
                read_csv_file(root, file, OutputType.JSON)
            if 'snippet_extra.csv' in file:
                read_csv_file(root, file, OutputType.PLIST)


if __name__ == '__main__':
    args = sys.argv
    process_input_dir(args[1])
