import argparse
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom


def createQrcFile(folderPath: str) -> None:
	root = ET.Element("RCC")
	root.set("version", "1.0")

	qresource = ET.SubElement(root, "qresource")

	for rootDir, _, files in os.walk(folderPath):
		for file in files:
			relativePath = os.path.relpath(os.path.join(rootDir, file), folderPath)
			fileElement = ET.SubElement(qresource, "file")
			fileElement.text = os.path.basename(folderPath) + "/" + relativePath

	xmlStr = minidom.parseString(ET.tostring(root)).toprettyxml(indent="    ")
	qrcPath = os.path.join(os.path.dirname(folderPath), "resources.qrc")
	with open(qrcPath, "w") as f:
		f.write(xmlStr)


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description="Generate resources_rc.py from a folder of resources.")
	parser.add_argument("folderPath", help="Path to the folder containing resource files")

	args = parser.parse_args()

	createQrcFile(args.folderPath)
