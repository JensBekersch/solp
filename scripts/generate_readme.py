import os
import re


def extract_readme_sections(lib_base_dir):
    readme_sections = []

    for root, _, files in os.walk(lib_base_dir):
        for file in files:
            if file.endswith(".py"):
                filepath = os.path.join(root, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    lines = f.readlines()

                i = 0
                while i < len(lines):
                    line = lines[i]
                    match = re.match(r"#\s*readme:\s+(.*)", line)
                    if match:
                        title = match.group(1).strip()
                        content_lines = []
                        i += 1
                        while (
                            i < len(lines)
                            and lines[i].lstrip().startswith("#")
                            and not re.match(r"#\s*readme:", lines[i])
                        ):
                            content_lines.append(lines[i].lstrip("#").strip())
                            i += 1
                        readme_sections.append((title, content_lines))
                    else:
                        i += 1

    return readme_sections


def write_readme(sections, output_file="README.md"):
    with open(output_file, "w", encoding="utf-8") as f:
        for title, content in sections:
            f.write(f"## {title}\n\n")
            for line in content:
                f.write(f"{line}\n")
            f.write("\n")


if __name__ == "__main__":
    base_path = os.path.abspath(os.path.dirname(__file__))
    start_dir = os.path.join(base_path, "..", "solp")
    sections = extract_readme_sections(start_dir)
    write_readme(sections)
    print("✅ README.md wurde generiert.")
