# WRITTEN BY Katherine Chan, Thomas Ruby, Jonathan Zhang

import xml.etree.ElementTree as ET
import os
import re

directory = "user_gestures"

def get_files(directory):
    files = []

    for filename in os.listdir(directory):
        f = os.path.join(directory, filename)
        if os.path.isfile(f):
            print(f)
            files.append(f)

    return files

def process_files(files):
    for file_name in files:
        tree = ET.parse(file_name)
        root = tree.getroot()
        # print(ET.tostring(root, encoding="utf8").decode("utf8"))

        gesture_name = re.search("[a-z-_]+\d+\.xml", file_name).group(0)[0:-4]
        gesture_name = gesture_name[:-1] + "0" + gesture_name[-1]
        subject_num = re.search("\d+", file_name).group(0)
        point_count = len(root.findall(".//Point"))

        root.set("Name", gesture_name)
        root.set("Subject", subject_num)
        root.set("NumPts", str(point_count))

        points = root.findall(".//Point")
        for i, point in enumerate(points):
            point.set("T", str(i))

        new_tree = ET.ElementTree(root)
        new_tree.write(file_name, encoding="utf-8", xml_declaration=True)
        
    return

for filename in os.listdir(directory):
    f = os.path.join(directory, filename)

    if os.path.isdir(f):
        files = get_files(f)
        process_files(files)