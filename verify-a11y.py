import re

with open('project-builder.html', 'r') as f:
    content = f.read()

count = content.count('aria-label="Remove row"')
print(f"Found {count} buttons with aria-label='Remove row'")
