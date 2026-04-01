import os
from mdtohtml import markdown_to_html_node

def extract_title(markdown):
    lines = markdown.splitlines()
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("No h1 header found in markdown")

def generate_page(from_path, template_path, dest_path):
    try:
        print(f"Generating page from {from_path} to {dest_path} using {template_path}")

        with open(from_path, "r") as f:
            md_content = f.read()

        with open(template_path, "r") as f:
            template = f.read()

        title = extract_title(md_content)
        template = template.replace("{{ Title }}", title)

        html_node = markdown_to_html_node(md_content)
        html_string = html_node.to_html()


        template = template.replace("{{ Content }}", html_string)

        if not os.path.exists(os.path.dirname(dest_path)):
            os.makedirs(os.path.dirname(dest_path))

        with open(dest_path, "w") as f:
            f.write(template)

    except Exception as e:
        print(f"Failed to generate page. Reason: {e}")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    for entry in os.listdir(dir_path_content):
        entry_path = os.path.join(dir_path_content, entry)
        if os.path.isdir(entry_path):
            generate_pages_recursive(entry_path, template_path, os.path.join(dest_dir_path, entry))
        elif entry.endswith(".md"):
            generate_page(entry_path, template_path, os.path.join(dest_dir_path, entry.replace(".md", ".html")))
    