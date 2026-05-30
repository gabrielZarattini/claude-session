#!/usr/bin/env python3
import os
import re
import sys
from datetime import datetime

# Directories configuration
VAULT_DIR = r"c:\Users\gabri\Documents\dev\MCORCH_CLAUDE\AI Sessions"
CLAUDE_DIR = os.path.join(VAULT_DIR, "ClaudeSessions")
GEMINI_DIR = os.path.join(VAULT_DIR, "GeminiSessions")
MOC_PATH = os.path.join(VAULT_DIR, "Sessions MOC.md")

# Excluded titles and generic patterns
UUID_RE = re.compile(r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$', re.IGNORECASE)
AGENT_RE = re.compile(r'^agent-[0-9a-f]+$', re.IGNORECASE)
DATE_PREFIX_RE = re.compile(r'^(\d{4}-\d{2}-\d{2})\s*-\s*(.*)$')

EXCLUDED_TITLES = {
    'handson', 'untitled session', 'userrequest', 'untitled', 
    'handson ainda estou esperando o webhook', 'meu banco de dados dos wordpress',
    'você se lembra que criamos um'
}

def parse_frontmatter(content):
    meta = {}
    if not content.startswith("---"):
        return meta
    parts = content.split("---")
    if len(parts) < 3:
        return meta
    fm_text = parts[1]
    
    current_key = None
    for line in fm_text.split("\n"):
        line = line.strip()
        if not line:
            continue
        
        # List items (e.g. - alias1)
        if line.startswith("-") and current_key:
            val = line[1:].strip().strip('"\'')
            if current_key in meta:
                if isinstance(meta[current_key], list):
                    meta[current_key].append(val)
                else:
                    meta[current_key] = [meta[current_key], val]
            else:
                meta[current_key] = [val]
            continue
            
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip()
            val = val.strip().strip('"\'')
            current_key = key
            
            # Inline lists (e.g., [tag1, tag2])
            if val.startswith("[") and val.endswith("]"):
                items = [i.strip().strip('"\'') for i in val[1:-1].split(",") if i.strip()]
                meta[key] = items
            elif not val:
                meta[key] = []
            else:
                meta[key] = val
    return meta

def mask_text(content):
    placeholders = []
    
    # Combined regex to match elements that SHOULD NOT be linked:
    # 1. Frontmatter at start of file
    # 2. Code blocks (```...```)
    # 3. Inline code (`...`)
    # 4. Existing wikilinks ([[...]])
    # 5. Markdown links ([...](...))
    # 6. HTML tags (<...>)
    combined_pattern = re.compile(
        r'(^---[\s\S]*?\n---)'                       # Frontmatter
        r'|(```[\s\S]*?```)'                         # Fenced code block
        r'|(`[^`\n]*?`)'                             # Inline code
        r'|(\[\[[\s\S]*?\]\])'                       # Wikilink
        r'|(\[[^\]\n]*?\]\([^)\n]*?\))'              # Markdown link
        r'|(<[^>\n]*?>)',                            # HTML tag
        re.MULTILINE
    )
    
    def replace_with_placeholder(match):
        val = match.group(0)
        idx = len(placeholders)
        placeholders.append(val)
        return f"___MASKED_BLOCK_{idx}___"
        
    masked_content = combined_pattern.sub(replace_with_placeholder, content)
    return masked_content, placeholders

def unmask_text(masked_content, placeholders):
    result = masked_content
    for idx, val in enumerate(placeholders):
        result = result.replace(f"___MASKED_BLOCK_{idx}___", val)
    return result

def collect_notes():
    note_catalog = []
    directories = [
        ("ClaudeSessions", CLAUDE_DIR),
        ("GeminiSessions", GEMINI_DIR)
    ]
    
    for folder_name, path in directories:
        if not os.path.exists(path):
            print(f"Warning: Directory {path} does not exist. Skipping.")
            continue
            
        for file in os.listdir(path):
            if not file.endswith(".md"):
                continue
                
            file_path = os.path.join(path, file)
            note_title = file[:-3] # Remove '.md'
            
            # Read content to parse frontmatter
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
            except Exception as e:
                print(f"Error reading {file}: {e}")
                continue
                
            meta = parse_frontmatter(content)
            
            # Analyze date prefix
            date_str = None
            topic_title = note_title
            date_match = DATE_PREFIX_RE.match(note_title)
            if date_match:
                date_str = date_match.group(1)
                topic_title = date_match.group(2)
                
            # Determine if this is a UUID/Agent/Excluded note
            is_generic = (
                UUID_RE.match(topic_title) or 
                AGENT_RE.match(topic_title) or 
                topic_title.lower() in EXCLUDED_TITLES or 
                len(topic_title) < 5
            )
            
            patterns = []
            # We always allow matching by the full note name (with date)
            patterns.append(note_title)
            
            # If not generic, we can match by descriptive topic title and aliases
            if not is_generic:
                patterns.append(topic_title)
                # Add aliases if they exist
                aliases = meta.get("aliases", [])
                if isinstance(aliases, list):
                    patterns.extend(aliases)
                elif isinstance(aliases, str) and aliases:
                    patterns.append(aliases)
            
            # Deduplicate and filter empty patterns
            patterns = list(set([p.strip() for p in patterns if p and len(p.strip()) >= 3]))
            
            note_catalog.append({
                "filename": file,
                "note_title": note_title,
                "folder": folder_name,
                "file_path": file_path,
                "date": date_str,
                "meta": meta,
                "is_generic": is_generic,
                "patterns": patterns
            })
            
    return note_catalog

def run_linking(note_catalog, dry_run=True):
    # Flatten patterns into a list of tuples: (pattern_str, note_title, note_file_path)
    pattern_list = []
    for note in note_catalog:
        for pattern in note["patterns"]:
            pattern_list.append((pattern, note["note_title"], note["file_path"]))
            
    # Sort patterns by length descending to match longest terms first
    pattern_list.sort(key=lambda x: len(x[0]), reverse=True)
    
    # Pre-compile regexes for each pattern
    compiled_patterns = []
    for pattern, dest_title, dest_path in pattern_list:
        pattern_escaped = re.escape(pattern)
        # Using custom word boundary to support Portuguese accent letters
        pattern_re = re.compile(rf'(?<!\w)({pattern_escaped})(?!\w)', re.IGNORECASE)
        compiled_patterns.append((pattern_re, dest_title, dest_path))
        
    # Group notes by folder to build separate chronological chains
    folder_groups = {}
    for note in note_catalog:
        folder = note["folder"]
        if folder not in folder_groups:
            folder_groups[folder] = []
        folder_groups[folder].append(note)
        
    # Sort key for chronological timeline: (1, date) if date exists, else (0, filename)
    def get_chron_sort_key(n):
        return (1, n["date"], n["filename"]) if n["date"] else (0, n["filename"], "")
        
    timeline_map = {} # Maps file_path -> (prev_note_title, next_note_title)
    for folder, folder_notes in folder_groups.items():
        sorted_notes = sorted(folder_notes, key=get_chron_sort_key)
        L = len(sorted_notes)
        for i in range(L):
            note = sorted_notes[i]
            prev_title = sorted_notes[i-1]["note_title"] if i > 0 else None
            next_title = sorted_notes[i+1]["note_title"] if i < L - 1 else None
            timeline_map[note["file_path"]] = (prev_title, next_title)
    
    links_created_count = 0
    modified_files_count = 0
    timeline_re = re.compile(r'\n*%% --- TIMELINE START --- %%.*?%% --- TIMELINE END --- %%', re.DOTALL)
    
    print(f"\n--- Running Auto-Linking (Dry-run: {dry_run}) ---")
    
    for target_note in note_catalog:
        file_path = target_note["file_path"]
        note_title = target_note["note_title"]
        
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            continue
            
        # Strip existing timeline block
        stripped_content = timeline_re.sub('', content).strip()
        
        # Build and append new timeline block
        prev_title, next_title = timeline_map.get(file_path, (None, None))
        timeline_block = ""
        if prev_title or next_title:
            lines = []
            lines.append("%% --- TIMELINE START --- %%")
            lines.append("> [!info] Linha do Tempo (Handoff)")
            if prev_title:
                lines.append(f"> * **Sessão Anterior**: [[{prev_title}]]")
            if next_title:
                lines.append(f"> * **Próxima Sessão**: [[{next_title}]]")
            lines.append("%% --- TIMELINE END --- %%")
            timeline_block = "\n".join(lines)
            
        updated_content = stripped_content
        if timeline_block:
            updated_content = stripped_content + "\n\n---\n\n" + timeline_block + "\n"
            
        # Check if timeline changed
        timeline_changed = (updated_content != content)
            
        masked_content, placeholders = mask_text(updated_content)
        original_masked = masked_content
        
        # Apply replacement patterns using pre-compiled regexes
        for pattern_re, dest_title, dest_path in compiled_patterns:
            # Do not link a note to itself
            if dest_path == file_path:
                continue
                
            # Perform regex substitution and count replacements
            new_content, count = pattern_re.subn(rf"[[{dest_title}|\1]]", masked_content)
            if count > 0:
                # Mask newly created wikilinks immediately to prevent nested replacements
                def mask_new_links(match):
                    idx = len(placeholders)
                    placeholders.append(match.group(0))
                    return f"___MASKED_BLOCK_{idx}___"
                
                wikilink_pattern = re.compile(r'\[\[[\s\S]*?\]\]')
                masked_content = wikilink_pattern.sub(mask_new_links, new_content)
                links_created_count += count
                
        # Write back if either the semantic links changed or the timeline block changed/was added
        has_changed = (masked_content != original_masked) or timeline_changed
        if has_changed:
            modified_files_count += 1
            final_content = unmask_text(masked_content, placeholders)
            
            if not dry_run:
                try:
                    with open(file_path, "w", encoding="utf-8") as f:
                        f.write(final_content)
                except Exception as e:
                    print(f"Error writing {file_path}: {e}")
            else:
                # Print dry-run diff summary
                print(f"[Dry-Run] Would modify: {target_note['folder']}/{target_note['filename']}")
                
    print(f"\nSummary of Linking:")
    print(f"- Total notes scanned: {len(note_catalog)}")
    print(f"- Files that will be/were modified: {modified_files_count}")
    print(f"- Total link edges created: {links_created_count}")

def generate_moc(note_catalog, dry_run=True):
    print(f"\n--- Generating Sessions MOC (Dry-run: {dry_run}) ---")
    
    # Sort notes chronologically by date descending
    # Notes without a valid date prefix will go to the end
    def get_sort_key(note):
        date_val = note["date"]
        if date_val:
            return (1, date_val)
        return (0, "")
        
    sorted_notes = sorted(note_catalog, key=get_sort_key, reverse=True)
    
    # Group notes by Year and Month
    chronological_groups = {}
    topic_groups = {
        "Supabase & Database": [],
        "JWT & Authentication": [],
        "TTS & Voice": [],
        "Orchestration & Agent System (MCORCH/Constellation)": [],
        "UI Extensions & Layouts": [],
        "Security & Credentials": [],
        "Other Sessions": []
    }
    
    for note in sorted_notes:
        # Chronological grouping
        date_str = note["date"]
        month_year = "Undated Sessions"
        if date_str:
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d")
                # Portuguese month names
                months_pt = [
                    "", "Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho",
                    "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"
                ]
                month_year = f"{months_pt[dt.month]} {dt.year}"
            except:
                pass
                
        if month_year not in chronological_groups:
            chronological_groups[month_year] = []
        chronological_groups[month_year].append(note)
        
        # Topic grouping based on tags and keywords in title
        tags = note["meta"].get("tags", [])
        if not isinstance(tags, list):
            tags = [tags] if tags else []
            
        tags_str = " ".join([t.lower() for t in tags])
        title_lower = note["note_title"].lower()
        
        # Categorization heuristics
        if "supabase" in tags_str or "supabase" in title_lower or "database" in tags_str or "migration" in tags_str:
            topic_groups["Supabase & Database"].append(note)
        elif "jwt" in tags_str or "jwt" in title_lower or "auth" in tags_str or "authentication" in title_lower:
            topic_groups["JWT & Authentication"].append(note)
        elif "tts" in tags_str or "tts" in title_lower or "voice" in tags_str or "audio" in title_lower or "kore" in title_lower:
            topic_groups["TTS & Voice"].append(note)
        elif "mcorch" in tags_str or "mcorch" in title_lower or "orchestra" in title_lower or "constelação" in title_lower or "agent" in tags_str:
            topic_groups["Orchestration & Agent System (MCORCH/Constellation)"].append(note)
        elif "ui" in tags_str or "layout" in tags_str or "layout" in title_lower or "overflow" in title_lower or "canvas" in title_lower:
            topic_groups["UI Extensions & Layouts"].append(note)
        elif "leak" in tags_str or "credential" in tags_str or "secret" in tags_str or "key" in title_lower:
            topic_groups["Security & Credentials"].append(note)
        else:
            topic_groups["Other Sessions"].append(note)
            
    # Construct MOC Markdown Content
    moc_lines = []
    moc_lines.append("---")
    moc_lines.append("type: MOC")
    moc_lines.append("tags:")
    moc_lines.append("  - hub/sessions")
    moc_lines.append("  - index")
    moc_lines.append("---")
    moc_lines.append("")
    moc_lines.append("# 🌟 AI Sessions - Map of Content (MOC)")
    moc_lines.append("")
    moc_lines.append("Este MOC atua como o diretório central do vault, organizando automaticamente todos os registros e transcrições de sessões de pair-programming com Claude e Gemini.")
    moc_lines.append("")
    moc_lines.append("> [!info] Métricas do Grafo")
    moc_lines.append(f"> * **Total de Sessões Registradas**: {len(note_catalog)}")
    moc_lines.append(f"> * **Sessões do Claude**: {len([n for n in note_catalog if n['folder'] == 'ClaudeSessions'])}")
    moc_lines.append(f"> * **Sessões do Gemini**: {len([n for n in note_catalog if n['folder'] == 'GeminiSessions'])}")
    moc_lines.append("")
    moc_lines.append("---")
    moc_lines.append("")
    moc_lines.append("## 📂 Tópicos e Categorias Principais")
    moc_lines.append("")
    
    for category, notes in topic_groups.items():
        if not notes:
            continue
        moc_lines.append(f"### {category}")
        for note in notes[:12]: # Limit to top 12 to avoid overwhelming MOC page size
            folder_prefix = "ClaudeSessions" if note["folder"] == "ClaudeSessions" else "GeminiSessions"
            moc_lines.append(f"*   `[[{note['note_title']}]]` - *{note['date'] or 'Sem data'}*")
        if len(notes) > 12:
            moc_lines.append(f"*   *... e mais {len(notes) - 12} sessões nessa categoria.*")
        moc_lines.append("")
        
    moc_lines.append("---")
    moc_lines.append("")
    moc_lines.append("## 📅 Índice Cronológico")
    moc_lines.append("")
    
    # Chronological display
    # Sort chronological groups by date (recent first)
    sorted_groups = sorted(chronological_groups.items(), reverse=True)
    for group_name, notes in sorted_groups:
        moc_lines.append(f"### {group_name}")
        for note in notes:
            moc_lines.append(f"*   `[[{note['note_title']}]]` ({note['folder']})")
        moc_lines.append("")
        
    moc_content = "\n".join(moc_lines)
    
    if not dry_run:
        try:
            with open(MOC_PATH, "w", encoding="utf-8") as f:
                f.write(moc_content)
            print(f"MOC file written successfully to {MOC_PATH}")
        except Exception as e:
            print(f"Error writing MOC file: {e}")
    else:
        print(f"[Dry-Run] Would write MOC containing {len(note_catalog)} links to {MOC_PATH}")

if __name__ == "__main__":
    dry_run = True
    if len(sys.argv) > 1 and sys.argv[1] == "--active":
        dry_run = False
        
    notes = collect_notes()
    run_linking(notes, dry_run=dry_run)
    generate_moc(notes, dry_run=dry_run)
