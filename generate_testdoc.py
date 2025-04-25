import os
import re
from collections import defaultdict

def extract_testdoc_sections(base_dir):
    testdoc_map = defaultdict(list)  # filename => [(title, [lines])]

    for root, _, files in os.walk(base_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i]
                    match = re.match(r"#\s*testdoc:\s+(.*)", line)
                    if match:
                        title = match.group(1).strip()
                        content_lines = []
                        i += 1
                        while i < len(lines) and lines[i].lstrip().startswith("#") and not re.match(r"#\s*testdoc:", lines[i]):
                            content_lines.append(lines[i].lstrip("#").strip())
                            i += 1
                        testdoc_map[file].append((title, content_lines))
                    else:
                        i += 1

    return testdoc_map


def write_testdoc(sections_by_file, output_file="TESTDOC.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Testdokumentation (automatisch generiert)\n\n")

        for filename in sorted(sections_by_file.keys()):
            f.write(f"## {filename}\n\n")
            for title, content in sections_by_file[filename]:
                f.write(f"### {title}\n\n")
                for line in content:
                    f.write(f"{line}\n")
                f.write("\n")
            f.write("\n---\n\n")


if __name__ == "__main__":
    base_dir = "test"
    sections = extract_testdoc_sections(base_dir)
    write_testdoc(sections)
    print("✅ TESTDOC.md wurde generiert mit Dateinamen als Überschriften.")
