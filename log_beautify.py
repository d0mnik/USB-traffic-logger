#/usr/bin/env python3

# imports
import argparse

parser = argparse.ArgumentParser(description="USB log beautifier")
parser.add_argument("filename",help="Filename to be parsed")
to_parse = parser.parse_args().filename
with open(to_parse,"r") as parse:
    log = parse.readlines()[1:]
    parse.close()
all_text = [i.strip("\n") for i in log if i.strip("\n") != ""]
created_files = [i for i in all_text if "created" in i]
deleted_files = [i for i in all_text if "deleted" in i]
print("\n---------------------")
print("Files Created: {}".format(len(created_files)))
print("---------------------\n")
for i in created_files:
    print(i.split(" ")[0])
print("\n---------------------")
print("Files Deleted: {}".format(len(deleted_files)))
print("---------------------\n")
for i in deleted_files:
    print(i.split(" ")[0])

