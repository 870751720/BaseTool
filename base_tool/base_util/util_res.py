import argparse
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def create_qrc_file(folder_path: str) -> None:
	root = ET.Element("RCC")
	root.set("version", "1.0")

	qresource = ET.SubElement(root, "qresource")

	for root_dir, _, files in os.walk(folder_path):
		for file in files:
			relative_path = os.path.relpath(
				os.path.join(root_dir, file), folder_path
			)
			file_element = ET.SubElement(qresource, "file")
			file_element.text = os.path.basename(folder_path) + "/" + relative_path

	xml_str = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
	qrc_path = os.path.join(os.path.dirname(folder_path), "resources.qrc")
	with open(qrc_path, "w") as f:
		f.write(xml_str)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(
		description="Generate resources_rc.py from a folder of resources."
	)
	parser.add_argument(
		"folder_path", help="Path to the folder containing resource files"
	)

	args = parser.parse_args()

	create_qrc_file(args.folder_path)
