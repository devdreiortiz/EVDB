import json
import os
import re

ECOSYS = os.path.join(os.path.dirname(__file__), 'ecosys')

def extract_meta(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        title = (lines[0] or '').replace('#', '').strip() if lines else ''
        category = ''
        level = ''
        desc = ''
        for i in range(min(len(lines), 30)):
            l = lines[i]
            if l.startswith('**Categoría:**'): category = l.replace('**Categoría:**', '').strip()
            if l.startswith('**Nivel de Autonomía:**'): level = l.replace('**Nivel de Autonomía:**', '').strip()
            if l.startswith('**Nivel de Complejidad:**'): level = l.replace('**Nivel de Complejidad:**', '').strip()
            if l.startswith('**Tipo:**'): category = l.replace('**Tipo:**', '').strip()
            if l.startswith('**Compatibilidad:**'): level = l.replace('**Compatibilidad:**', '').strip()
        for i in range(1, min(len(lines), 25)):
            l = lines[i].strip()
            if not l or l.startswith('---') or l.startswith('```') or re.match(r'^##\s+\d', l) or l.startswith('- ') or l.startswith('"'):
                continue
            cleaned = l.replace('**', '').strip()
            if cleaned and len(cleaned) > 25 and 'Categoría' not in cleaned and 'Nivel de' not in cleaned and 'Tipo:' not in cleaned and 'Compatibilidad' not in cleaned and 'skill_id' not in cleaned and '"version"' not in cleaned:
                desc = cleaned[:200]
                break
        return {'title': title, 'category': category, 'level': level, 'desc': desc}
    except:
        return {'title': '', 'category': '', 'level': '', 'desc': ''}

def readable_name(name):
    name = re.sub(r'\.(md|txt)$', '', name)
    name = re.sub(r'^Prompt_', '', name)
    name = re.sub(r'^Skill_', '', name)
    name = re.sub(r'^Agente_', '', name)
    name = name.replace('_', ' ')
    name = re.sub(r'([a-z])([A-Z])', r'\1 \2', name)
    name = re.sub(r'\b(De|Del|La)\b', lambda m: m.group(1).lower(), name)
    return name

def scan_dir(dirpath, parent_id=''):
    try:
        entries = sorted(os.listdir(dirpath))
    except:
        return []
    entries = [e for e in entries if e != 'builder.py']
    groups = []
    prompts = []
    for entry in entries:
        full_path = os.path.join(dirpath, entry)
        rel_path = '/' + os.path.relpath(full_path, os.path.dirname(__file__)).replace('\\', '/')
        if os.path.isdir(full_path):
            children = scan_dir(full_path, entry)
            if children:
                node_id = (parent_id + '-' + entry).lower()
                node_id = re.sub(r'[^a-z0-9-]', '-', node_id)
                node_id = re.sub(r'-+', '-', node_id)
                groups.append({
                    'id': node_id,
                    'label': readable_name(entry),
                    'type': 'group',
                    'count': len(children),
                    'children': children,
                })
        elif entry.endswith('.md') or entry.endswith('.txt'):
            meta = extract_meta(full_path) if entry.endswith('.md') else {'title': '', 'category': '', 'level': '', 'desc': ''}
            with open(full_path, 'r', encoding='utf-8') as f:
                content = f.read()
            node_id = (parent_id + '-' + entry).lower()
            node_id = re.sub(r'[^a-z0-9-]', '-', node_id)
            node_id = re.sub(r'-+', '-', node_id)
            prompts.append({
                'id': node_id,
                'label': readable_name(entry),
                'type': 'prompt',
                'file': entry,
                'prompt': rel_path,
                'abspath': full_path,
                'content': content,
                'meta': meta,
            })
    if groups and prompts:
        node_id = (parent_id + '-general').lower()
        node_id = re.sub(r'[^a-z0-9-]', '-', node_id)
        node_id = re.sub(r'-+', '-', node_id)
        groups.append({
            'id': node_id,
            'label': 'General',
            'type': 'group',
            'count': len(prompts),
            'children': prompts,
        })
        groups.sort(key=lambda x: x['label'])
        return groups
    nodes = groups + prompts
    nodes.sort(key=lambda x: (0 if x['type'] == 'group' else 1, x['label']))
    return nodes

folders = ['Agentes', 'Prompts', 'Skills']
result = {}
for f in folders:
    dir_path = os.path.join(ECOSYS, f)
    if os.path.isdir(dir_path):
        result[f] = scan_dir(dir_path, f)

extra_dir = os.path.join(ECOSYS, 'Agents')
if os.path.isdir(extra_dir):
    extra = scan_dir(extra_dir, 'Agentes')
    if extra:
        result['Agentes'].append({
            'id': 'agentes-standalone',
            'label': 'Standalone Agents',
            'type': 'group',
            'count': len(extra),
            'children': extra,
        })

json_str = json.dumps(result, ensure_ascii=False)
outdir = os.path.dirname(__file__)
with open(os.path.join(outdir, 'tree-data.json'), 'w', encoding='utf-8') as f:
    json.dump(result, f, ensure_ascii=False, indent=2)
with open(os.path.join(outdir, 'tree-data.js'), 'w', encoding='utf-8') as f:
    f.write('window.__TREE__ = ' + json_str + ';')

def count_prompts(nodes):
    c = 0
    for n in nodes:
        if n['type'] == 'prompt':
            c += 1
        if 'children' in n:
            c += count_prompts(n['children'])
    return c

print('tree-data.json + tree-data.js regenerated')
for f in folders:
    items = result.get(f, [])
    total = count_prompts(items)
    print(f'  {f}: {len(items)} groups, {total} prompts')
