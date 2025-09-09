import os
import re
from pathlib import Path
from html.parser import HTMLParser
from html import escape

class HTMLFixer:
    def __init__(self):
        self.fixed_count = 0
        self.error_count = 0
        self.files_processed = 0
        
    def fix_malformed_attributes(self, content):
        """Fix malformed div attributes and other HTML issues"""
        # Fix the specific malformed div issue found in Gr6_55_E1_1_48.html
        # This regex finds divs with broken attributes
        pattern = r'<div\s+"this=.*?style="display:inline-block"[^>]*>'
        
        def replace_malformed_div(match):
            # Extract label if present
            label_match = re.search(r'label="([^"]+)"', match.group())
            if label_match:
                label = label_match.group(1)
                return f'<div class="item" label="{label}" style="display:inline-block">'
            return '<div class="item" style="display:inline-block">'
        
        content = re.sub(pattern, replace_malformed_div, content)
        
        # Fix any other malformed attributes (attributes with spaces or special chars)
        # Remove any attributes that look corrupted (contain $, =', etc.)
        content = re.sub(r'\s+\$[^=]+=\'[^\']*\'', '', content)
        content = re.sub(r'\s+[^\s=]+=[\'"][^\'"]*[\$][^\'"]*[\'"]', '', content)
        
        return content
    
    def ensure_proper_doctype(self, content):
        """Ensure all files have proper DOCTYPE and html tag"""
        # Check if DOCTYPE exists
        if not content.strip().startswith('<!DOCTYPE'):
            # Check if it starts with <html
            if content.strip().startswith('<html'):
                # Add DOCTYPE before html tag
                content = '<!DOCTYPE html>\n' + content
            else:
                # Add both DOCTYPE and html tag
                content = '<!DOCTYPE html>\n<html lang="en">\n' + content
        
        # Ensure html tag has lang attribute
        content = re.sub(r'<html(?:\s+[^>]*)?>', 
                        lambda m: '<html lang="en">' if 'lang=' not in m.group() else m.group(), 
                        content)
        
        return content
    
    def fix_unclosed_tags(self, content):
        """Ensure all tags are properly closed"""
        # Common self-closing tags that should be properly formatted
        self_closing_tags = ['img', 'br', 'hr', 'input', 'meta', 'link', 'area', 'base', 'col', 'embed', 'source', 'track', 'wbr']
        
        for tag in self_closing_tags:
            # Fix tags that aren't properly self-closed
            pattern = f'<{tag}([^>]*?)(?<!/)>'
            replacement = f'<{tag}\\1/>'
            content = re.sub(pattern, replacement, content, flags=re.IGNORECASE)
        
        return content
    
    def fix_svg_viewbox(self, content):
        """Fix SVG viewBox attribute (case-sensitive)"""
        # viewBox should be camelCase, not viewbox
        content = re.sub(r'viewbox=', 'viewBox=', content, flags=re.IGNORECASE)
        return content
    
    def validate_and_fix_quotes(self, content):
        """Ensure all attribute values are properly quoted"""
        # Fix unquoted attribute values
        # This regex finds attributes without quotes
        pattern = r'(\s+[a-zA-Z-]+)=([^"\s>]+)(?=[\s>])'
        
        def add_quotes(match):
            attr_name = match.group(1)
            attr_value = match.group(2)
            # Don't add quotes if value already has them
            if attr_value.startswith('"') or attr_value.startswith("'"):
                return match.group()
            return f'{attr_name}="{attr_value}"'
        
        content = re.sub(pattern, add_quotes, content)
        return content
    
    def clean_html_structure(self, content):
        """Ensure proper HTML structure"""
        # Check if file has proper closing tags
        if '<html' in content and '</html>' not in content:
            content += '\n</html>'
        
        if '<body' in content and '</body>' not in content:
            # Add closing body tag before closing html tag
            content = content.replace('</html>', '</body>\n</html>')
        
        if '<head' in content and '</head>' not in content:
            # Find where head section should end (usually before body)
            body_pos = content.find('<body')
            if body_pos > 0:
                content = content[:body_pos] + '</head>\n' + content[body_pos:]
        
        return content
    
    def format_html(self, content):
        """Basic formatting to make HTML more readable"""
        # Add newlines after major tags for readability
        tags_needing_newline = ['</head>', '<body', '</body>', '</html>', '<div', '</div>']
        
        for tag in tags_needing_newline:
            # Only add newline if not already present
            content = re.sub(f'({tag}[^>]*>)(?!\n)', r'\1\n', content)
        
        # Remove excessive blank lines (more than 2 consecutive)
        content = re.sub(r'\n{3,}', '\n\n', content)
        
        return content
    
    def fix_html_file(self, filepath):
        """Fix a single HTML file"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            original_content = content
            
            # Apply all fixes
            content = self.fix_malformed_attributes(content)
            content = self.ensure_proper_doctype(content)
            content = self.fix_unclosed_tags(content)
            content = self.fix_svg_viewbox(content)
            content = self.validate_and_fix_quotes(content)
            content = self.clean_html_structure(content)
            content = self.format_html(content)
            
            # Only write if content changed
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                self.fixed_count += 1
                return True
            return False
            
        except Exception as e:
            print(f"Error processing {filepath}: {str(e)}")
            self.error_count += 1
            return False
    
    def process_all_files(self, directory):
        """Process all HTML files in the directory"""
        html_files = list(Path(directory).glob('*.html'))
        total_files = len(html_files)
        
        print(f"Found {total_files} HTML files to process...")
        print("-" * 50)
        
        for i, filepath in enumerate(html_files, 1):
            self.files_processed += 1
            was_fixed = self.fix_html_file(filepath)
            
            # Progress indicator every 100 files
            if i % 100 == 0:
                print(f"Processed {i}/{total_files} files... ({self.fixed_count} fixed so far)")
        
        print("-" * 50)
        print(f"\nProcessing complete!")
        print(f"Total files processed: {self.files_processed}")
        print(f"Files fixed: {self.fixed_count}")
        print(f"Files with errors: {self.error_count}")
        print(f"Files unchanged: {self.files_processed - self.fixed_count - self.error_count}")

def main():
    html_dir = r"C:\Users\kapil\numi-scraper\HTML"
    
    print("HTML File Fixer")
    print("=" * 50)
    print(f"Directory: {html_dir}")
    print("=" * 50)
    
    fixer = HTMLFixer()
    fixer.process_all_files(html_dir)
    
    print("\nAll HTML files have been processed and fixed!")

if __name__ == "__main__":
    main()