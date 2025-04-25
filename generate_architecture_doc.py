import os
import re


def extract_arc42_comments(lib_base_dir):
    arc_sections = []

    for root, _, files in os.walk(lib_base_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i]
                    match = re.match(r"#\s*arc42:\s*((?:\d+\.)*\d+)\s+(.*)",
                                     line)
                    if match:
                        section_id = match.group(1).strip()
                        section_title = match.group(2).strip()
                        description_lines = []
                        i += 1
                        while i < len(lines) and lines[i].lstrip().startswith(
                                "#") and not re.match(r"#\s*arc42:", lines[i]):
                            description_lines.append(
                                lines[i].lstrip("#").strip())
                            i += 1
                        arc_sections.append(
                            (section_id, section_title, description_lines))
                    else:
                        i += 1

    return arc_sections


def write_markdown(sections, output_file="ARCHITEKTUR.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        f.write("# Architekturübersicht (generiert aus Code-Kommentaren)\n\n")
        for section_id, title, description in sorted(
                sections,
                key=lambda x: list(map(int, x[0].split(".")))):
            f.write(f"## {section_id} {title}\n\n")
            for line in description:
                f.write(f"{line}\n")
            f.write("\n---\n\n")


if __name__ == "__main__":
    base_dir = "."
    sections = extract_arc42_comments(base_dir)
    write_markdown(sections)
    print("✅ ARCHITEKTUR.md wurde generiert.")
