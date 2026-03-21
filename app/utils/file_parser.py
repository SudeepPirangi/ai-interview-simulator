async def read_html_file(file_path: str):
    print("Reading HTML content from file", file_path)
    with open(file_path, "r") as f:
        html_content = f.read()
    return html_content
