with open('kreise-kurse.html', 'r') as f:
    lines = f.readlines()

# Find the start and end of the "Weitere Termine & Kreise 2026" section
start_idx = -1
end_idx = -1
for i, line in enumerate(lines):
    if 'Weitere Termine & Kreise 2026' in line:
        # Step back to the <section class="section">
        for j in range(i, -1, -1):
            if '<section class="section">' in lines[j]:
                start_idx = j
                break
        
        # Step forward to the </section>
        for j in range(i, len(lines)):
            if '</section>' in lines[j]:
                end_idx = j
                break
        break

if start_idx != -1 and end_idx != -1:
    section_lines = lines[start_idx:end_idx+1]
    
    # Modify the section lines:
    # 1. Title
    for i, line in enumerate(section_lines):
        if 'Weitere Termine & Kreise 2026' in line:
            section_lines[i] = line.replace('Weitere Termine & Kreise 2026', 'Termine & Kreise 2026')
        
        # Update links and buttons
        if 'Ahnenkreis "Wurzeln der Kraft"' in line:
            # The button is a few lines down
            for j in range(i, min(i+10, len(section_lines))):
                if 'Anmelden' in section_lines[j] or 'btn-secondary' in section_lines[j]:
                    section_lines[j] = section_lines[j].replace('#voranmeldung', '/ahnenkreis').replace('Anmelden', 'Mehr Infos')
                    
        if 'Meditationsabend Jenseits' in line:
            for j in range(i, min(i+10, len(section_lines))):
                if 'Anmelden' in section_lines[j] or 'btn-secondary' in section_lines[j]:
                    section_lines[j] = section_lines[j].replace('#voranmeldung', '/meditationsabend').replace('Anmelden', 'Mehr Infos')

        if 'Krafttier-Wochenende' in line:
            for j in range(i, min(i+10, len(section_lines))):
                if 'Anmelden' in section_lines[j] or 'btn-secondary' in section_lines[j]:
                    section_lines[j] = section_lines[j].replace('#voranmeldung', '/krafttier-wochenende').replace('Anmelden', 'Mehr Infos')
            
    # Delete original section
    del lines[start_idx:end_idx+1]
    
    # Find insertion point (before Highlight section)
    # The Highlight section has a comment: <!-- Highlight: Ausbildung & Workshop Wien 2026 -->
    insert_idx = -1
    for i, line in enumerate(lines):
        if '<!-- Highlight: Ausbildung & Workshop Wien 2026 -->' in line:
            insert_idx = i
            break
            
    if insert_idx != -1:
        # Add a comment and the section
        section_lines.insert(0, "    <!-- Termine und Kreise Overview -->\n")
        lines = lines[:insert_idx] + section_lines + lines[insert_idx:]
        
    with open('kreise-kurse.html', 'w') as f:
        f.writelines(lines)
    print("Successfully updated kreise-kurse.html")
else:
    print("Could not find the section")
