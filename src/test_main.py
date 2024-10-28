from main import extract_title, generate_page
import os
import pytest
import shutil

def test_extract_title():
    # Test valid title
    assert extract_title("# Hello World") == "Hello World"
    
    # Test title in code block
    md_with_code = """```
    # Not a title
    ```
    # Real Title
    """
    assert extract_title(md_with_code) == "Real Title"
    
    # Test no title
    try:
        extract_title("Not a title")
        assert False, "Should have raised exception"
    except Exception:
        assert True
        
def teardown_test_files():
    # Clean up test files after each test
    files = ["test_content.md", "test_template.html", "test_output.html"]
    for file in files:
        if os.path.exists(file):
            os.remove(file)
    if os.path.exists("nested"):
        shutil.rmtree("nested")

def test_generate_page_basic():
    try:
        with open("test_content.md", "w") as f:
            f.write("# Test Title\n**Bold** and *italic*")
        with open("test_template.html", "w") as f:
            f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")
        
        generate_page("test_content.md", "test_template.html", "test_output.html")
        
        with open("test_output.html", "r") as f:
            content = f.read()
            assert "<title>Test Title</title>" in content
            assert "<b>Bold</b>" in content
            assert "<i>italic</i>" in content
    finally:
        teardown_test_files()

def test_generate_page_complex_markdown():
    try:
        markdown_content = """# Complex Page
* List item 1
* List item 2

[Link](https://example.com)

> This is a blockquote

## Second Level Header

```python
def code():
    pass
```"""
        
        with open("test_content.md", "w") as f:
            f.write(markdown_content)
        with open("test_template.html", "w") as f:
            f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")
        
        generate_page("test_content.md", "test_template.html", "test_output.html")
        
        with open("test_output.html", "r") as f:
            content = f.read()
            assert "<title>Complex Page</title>" in content
            assert "<ul>" in content
            assert "<li>List item" in content
            assert "<a href=" in content
            assert "<blockquote>" in content
            assert "<code>" in content
            assert "<h2>" in content
    finally:
        teardown_test_files()

def test_generate_page_nested_directories():
    try:
        nested_path = "nested/deep/very/deep/output.html"
        
        with open("test_content.md", "w") as f:
            f.write("# Nested Test\nSome content")
        with open("test_template.html", "w") as f:
            f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")
        
        generate_page("test_content.md", "test_template.html", nested_path)
        
        # Check if file exists and contains correct content
        assert os.path.exists(nested_path)
        with open(nested_path, "r") as f:
            content = f.read()
            assert "<title>Nested Test</title>" in content
    finally:
        teardown_test_files()

def test_generate_page_ordered_lists():
    try:
        markdown_content = """# Lists Test
1. First item
2. Second item
3. Third item"""
        
        with open("test_content.md", "w") as f:
            f.write(markdown_content)
        with open("test_template.html", "w") as f:
            f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")
        
        generate_page("test_content.md", "test_template.html", "test_output.html")
        
        with open("test_output.html", "r") as f:
            content = f.read()
            assert "<ol>" in content
            assert "<li>First item</li>" in content
            assert "<li>Second item</li>" in content
    finally:
        teardown_test_files()
        
def test_generate_page_edge_cases():
    try:
        # Test empty markdown (should fail due to no h1)
        with open("test_content.md", "w") as f:
            f.write("")
        with open("test_template.html", "w") as f:
            f.write("<html><title>{{ Title }}</title><body>{{ Content }}</body></html>")
        
        with pytest.raises(Exception):
            generate_page("test_content.md", "test_template.html", "test_output.html")
            
        # Test markdown with only h1
        with open("test_content.md", "w") as f:
            f.write("# Just a title\n")
        generate_page("test_content.md", "test_template.html", "test_output.html")
        with open("test_output.html", "r") as f:
            content = f.read()
            assert "<title>Just a title</title>" in content
            
        # Test with multiple consecutive newlines
        with open("test_content.md", "w") as f:
            f.write("# Multiple Newlines\n\n\n\nSome content")
        generate_page("test_content.md", "test_template.html", "test_output.html")
        with open("test_output.html", "r") as f:
            content = f.read()
            assert "Multiple Newlines" in content
            assert "Some content" in content
            
    finally:
        teardown_test_files()
