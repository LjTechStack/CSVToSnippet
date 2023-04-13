# CSV To Snippet

#### Author: ljtechstack

___

The objective of this project is to transform
two CSV files into a format that conforms to the Alfred snippet file structure,
allowing them to be imported into Alfred.

This is a Python program that uses the csv and plistlib modules to read and process CSV files.
The program takes in CSV files containing data for Alfred snippets, and converts them into the appropriate format for
importing into the Alfred application.
It creates an output directory and subdirectories for each snippet folder specified in the CSV files, and generates JSON
files containing the snippet data.
If the CSV file specifies that the snippets should be in plist format, the program creates a property list file instead.
The program takes a command line argument specifying the input directory containing the CSV files to be processed.