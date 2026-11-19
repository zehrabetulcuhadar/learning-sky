import json
import pathlib
import xml.etree.ElementTree as ET

here = pathlib.Path(__file__).parent

from_json = json.loads((here / "post.json").read_text(encoding="utf-8"))

root = ET.parse(here / "post.xml").getroot()
from_xml = {
    "title": root.findtext("title"),
    "topic": root.findtext("topic"),
    "tags": [t.text for t in root.find("tags")],
    "draft": root.get("draft") == "true",  # XML has no booleans: everything is text until you convert it
    "country": root.findtext("country"),
}

print("JSON:", from_json)
print("XML: ", from_xml)
print("Same data:", from_json == from_xml)
print("\nYAML: needs `pip install pyyaml`. With a YAML 1.1 parser, an unquoted `country: NO` becomes False.")
