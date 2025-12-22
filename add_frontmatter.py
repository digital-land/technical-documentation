#!/usr/bin/env python3
"""
One-time script to add YAML frontmatter to all markdown files in the docs directory.
Extracts the first heading (# Title) and adds it as frontmatter at the top of the file.
"""

import os
import re
from pathlib import Path


def extract_first_heading(content):
    """Extract the first markdown heading from content."""
    lines = content.split('\n')
    for line in lines:
        # Match lines starting with one or more # (any heading level)
        match = re.match(r'^#+\s+(.+)$', line.strip())
        if match:
            return match.group(1).strip()
    return None


def has_frontmatter(content):
    """Check if content already has YAML frontmatter."""
    return content.startswith('---')


def add_frontmatter(filepath):
    """Add frontmatter to a markdown file if it doesn't already have it."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Skip if already has frontmatter
        if has_frontmatter(content):
            print(f"⏭️  Skipping {filepath} (already has frontmatter)")
            return False
        
        # Extract first heading
        title = extract_first_heading(content)
        if not title:
            print(f"⚠️  Warning: No heading found in {filepath}")
            return False
        
        # Remove the first heading from content
        lines = content.split('\n')
        new_lines = []
        heading_removed = False
        for line in lines:
            if not heading_removed and re.match(r'^#+\s+(.+)$', line.strip()):
                heading_removed = True
                continue
            new_lines.append(line)
        
        # Remove leading empty lines after heading removal
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)
        
        content_without_heading = '\n'.join(new_lines)
        
        # Create frontmatter
        frontmatter = f"---\ntitle: {title}\n---\n\n"
        new_content = frontmatter + content_without_heading
        
        # Write back to file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print(f"✅ Added frontmatter to {filepath}")
        return True
        
    except Exception as e:
        print(f"❌ Error processing {filepath}: {e}")
        return False


def main():
    """Process all markdown files in the docs directory."""
    docs_dir = Path(__file__).parent / 'docs'
    
    if not docs_dir.exists():
        print(f"Error: docs directory not found at {docs_dir}")
        return
    
    print(f"Scanning for markdown files in {docs_dir}...\n")
    
    # Find all .md files recursively
    md_files = list(docs_dir.rglob('*.md'))
    
    print(f"Found {len(md_files)} markdown files\n")
    
    modified_count = 0
    skipped_count = 0
    error_count = 0
    
    for md_file in sorted(md_files):
        result = add_frontmatter(md_file)
        if result is True:
            modified_count += 1
        elif result is False and has_frontmatter(md_file.read_text()):
            skipped_count += 1
        else:
            error_count += 1
    
    print(f"\n{'='*60}")
    print(f"Summary:")
    print(f"  ✅ Modified: {modified_count}")
    print(f"  ⏭️  Skipped: {skipped_count}")
    print(f"  ⚠️  Errors: {error_count}")
    print(f"{'='*60}")


if __name__ == '__main__':
    main()
