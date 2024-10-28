import os
import pathlib
from markdown_blocks import markdown_to_html_node
            
def generate_page(from_path, template_path, dest_path):
    print(f" * {from_path} {template_path} -> {dest_path}")
    from_file = open(from_path, "r")
    markdown_content = from_file.read()
    from_file.close()

    template_file = open(template_path, "r")
    template = template_file.read()
    template_file.close()

    node = markdown_to_html_node(markdown_content)
    html = node.to_html()

    title = extract_title(markdown_content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dest_dir_path = os.path.dirname(dest_path)
    if dest_dir_path != "":
        os.makedirs(dest_dir_path, exist_ok=True)
    to_file = open(dest_path, "w")
    to_file.write(template)


def extract_title(md):
    lines = md.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("No title found")


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    print(f"\nStarting recursive generation:")
    print(f"Content dir: {dir_path_content}")
    print(f"Template: {template_path}")
    print(f"Destination: {dest_dir_path}")
    
    # Create destination directory if it doesn't exist
    pathlib.Path(dest_dir_path).mkdir(parents=True, exist_ok=True)
    
    entries = os.listdir(dir_path_content)
    print(f"Found entries: {entries}")
    
    for entry in entries:
        current_path = os.path.join(dir_path_content, entry)
        relative_path = os.path.relpath(current_path, dir_path_content)
        dest_path = os.path.join(dest_dir_path, relative_path)
        
        print(f"\nProcessing: {entry}")
        print(f"Current path: {current_path}")
        print(f"Is file? {os.path.isfile(current_path)}")
        print(f"Destination path: {dest_path}")
        
        if os.path.isfile(current_path):
            if current_path.endswith('.md'):
                html_path = dest_path.replace('.md', '.html')
                print(f"HTML path: {html_path}")  # Move this inside the if block
                generate_page(current_path, template_path, html_path)
        else:
            # Create directory with parents
            pathlib.Path(dest_path).mkdir(parents=True, exist_ok=True)
            generate_pages_recursive(current_path, template_path, dest_path)
