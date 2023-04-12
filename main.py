import csv
import json
import os.path
import plistlib
import sys
import uuid

name_column = 0
keyword_column = 0
snippet_column = 0
folder_column = 0
folder_snip_column = 0
snippet_keyword_prefix_column = 0
snippet_keyword_suffix_column = 0


def parse_header_data(header, output_type):
    """Process header file of all files"""
    global name_column
    global keyword_column
    global snippet_column
    global folder_snip_column
    global folder_column
    global snippet_keyword_prefix_column
    global snippet_keyword_suffix_column

    for n in range(len(header)):
        if "name" == header[n]:
            name_column = n
        if "keyword" == header[n]:
            keyword_column = n
        if "snippet" == header[n]:
            snippet_column = n
        if "folder" == header[n]:
            if output_type == "json":
                folder_snip_column = n
            else:
                folder_column = n
        if "snippetkeywordprefix" == header[n]:
            snippet_keyword_prefix_column = n
        if "snippetkeywordsuffix" == header[n]:
            snippet_keyword_suffix_column = n


def snippet_maker(snippet_name, snippet_keyword, snippet, unique_id):
    """Define row"""
    snippet_dict = {"snippet": "" + snippet,
                    "uid": unique_id,
                    "name": snippet_name,
                    "keyword": snippet_keyword}
    print(snippet_dict)
    return {"alfredsnippet": snippet_dict}


def plist_maker(snippetkeywordprefix, snippetkeywordsuffix):
    plist_dict = {
        "snippetkeywordprefix": snippetkeywordprefix, "snippetkeywordsuffix": snippetkeywordsuffix
    }
    return plist_dict


def remove_existing_file(base_file_path, file_sub_string):
    """Removed existing file with other uniqueID pattern"""
    for filename in os.listdir(base_file_path):
        if file_sub_string + "[" in filename:
            os.remove(base_file_path + "/" + filename)


def process_csv_data(line_data, output_type):
    """Process the csv data"""
    name = line_data[name_column].strip()
    folder = line_data[folder_snip_column].strip() \
        if output_type == "json" else line_data[folder_column].strip()
    snippet_keyword = line_data[keyword_column].strip()
    snippet = line_data[snippet_column].strip()
    snippet_keyword_prefix = line_data[snippet_keyword_prefix_column].strip()
    snippet_keyword_suffix = line_data[snippet_keyword_suffix_column].strip()
    unique_id = uuid.uuid4()
    root = "output"
    if not os.path.isdir(root):
        os.mkdir(root)
    root = "output/snippets"
    if not os.path.isdir(root):
        os.mkdir(root)
    base_path = root + "/" + folder
    if not os.path.isdir(base_path):
        os.mkdir(base_path)

    remove_existing_file(base_path, name)

    if output_type == "json":
        with open(base_path + '/' + name + '[' + str(unique_id) + "].json", "w",
                  encoding="utf8") as outfile:
            json.dump(snippet_maker(name, snippet_keyword, snippet, str(unique_id)), outfile)
    if output_type == "plist":
        with open(base_path + "/info.plist", "wb") as outfile:
            plistlib.dump(plist_maker(snippet_keyword_prefix, snippet_keyword_suffix), outfile)


def read_csv_file(root, csv_file_name):
    """Read content of csv file"""
    with open(os.path.join(root, csv_file_name)) as csv_file:
        csvreader = csv.reader(csv_file, delimiter="\t")
        parse_header_data(next(csvreader), "json")
        for line in csv.reader(csv_file, delimiter="\t"):
            process_csv_data(line, "json")


def read_plist_file(root, csv_file_name):
    with open(os.path.join(root, csv_file_name)) as csv_file:
        csvreader = csv.reader(csv_file, delimiter="\t")
        parse_header_data(next(csvreader), "plist")
        for line in csv.reader(csv_file, delimiter="\t"):
            process_csv_data(line, "plist")


def process_input_dir(input_dir):
    """Loop thought input directory"""
    for (root, path, files) in os.walk(input_dir):
        for file in files:
            if 'snippet.csv' in file:
                read_csv_file(root, file)
            if 'snippet_extra.csv' in file:
                read_plist_file(root, file)


# Work on after SnippetToCSV
if __name__ == '__main__':
    args = sys.argv
    process_input_dir(args[1])
