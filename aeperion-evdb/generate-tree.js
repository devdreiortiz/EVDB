const fs = require('fs')
const path = require('path')

const ECOSYS = path.join(__dirname, 'ecosys')

function extractMeta(filePath) {
  try {
    const content = fs.readFileSync(filePath, 'utf-8')
    const lines = content.split('\n')
    const title = (lines[0] || '').replace(/^#\s+/, '').trim()

    let category = ''
    let level = ''
    let desc = ''

    for (let i = 0; i < Math.min(lines.length, 30); i++) {
      const l = lines[i]
      if (l.startsWith('**Categoría:**')) category = l.replace('**Categoría:**', '').trim()
      if (l.startsWith('**Nivel de Autonomía:**')) level = l.replace('**Nivel de Autonomía:**', '').trim()
      if (l.startsWith('**Nivel de Complejidad:**')) level = l.replace('**Nivel de Complejidad:**', '').trim()
      if (l.startsWith('**Tipo:**')) category = l.replace('**Tipo:**', '').trim()
      if (l.startsWith('**Compatibilidad:**')) level = l.replace('**Compatibilidad:**', '').trim()
    }

    for (let i = 1; i < Math.min(lines.length, 25); i++) {
      const l = lines[i].trim()
      if (!l || l.startsWith('---') || l.startsWith('```') || l.match(/^##\s+\d/) || l.startsWith('- ') || l.startsWith('"')) continue
      const cleaned = l.replace(/\*\*/g, '').trim()
      if (cleaned && cleaned.length > 25 && !cleaned.includes('Categoría') && !cleaned.includes('Nivel de') && !cleaned.includes('Tipo:') && !cleaned.includes('Compatibilidad') && !cleaned.includes('skill_id') && !cleaned.includes('"version"')) {
        desc = cleaned.substring(0, 200)
        break
      }
    }

    return { title, category, level, desc }
  } catch {
    return { title: '', category: '', level: '', desc: '' }
  }
}

function readableName(file) {
  let name = file.replace(/\.md$/, '').replace(/\.txt$/, '')
  name = name.replace(/^Prompt_/, '')
  name = name.replace(/^Skill_/, '')
  name = name.replace(/^Agente_/, '')
  name = name.replace(/_/g, ' ')
  name = name.replace(/([a-z])([A-Z])/g, '$1 $2')
  name = name.replace(/De /g, 'de ').replace(/Del /g, 'del ').replace(/La /g, 'la ')
  return name
}

function scanDir(dir, parentId = '') {
  const entries = fs.readdirSync(dir, { withFileTypes: true }).filter(e => e.name !== 'builder.py')
  const groups = []
  const prompts = []

  for (const entry of entries) {
    const fullPath = path.join(dir, entry.name)
    const relPath = '/' + path.relative(__dirname, fullPath).replace(/\\/g, '/')

    if (entry.isDirectory()) {
      const children = scanDir(fullPath, entry.name)
      if (children.length > 0) {
        groups.push({
          id: (parentId + '-' + entry.name).replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase().replace(/-+/g, '-'),
          label: readableName(entry.name),
          type: 'group',
          count: children.length,
          children,
        })
      }
    } else if (entry.isFile() && (entry.name.endsWith('.md') || entry.name.endsWith('.txt'))) {
      const meta = entry.name.endsWith('.md') ? extractMeta(fullPath) : { title: '', category: '', level: '', desc: '' }
      const content = fs.readFileSync(fullPath, 'utf-8')
      prompts.push({
        id: (parentId + '-' + entry.name).replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase().replace(/-+/g, '-'),
        label: readableName(entry.name),
        type: 'prompt',
        file: entry.name,
        prompt: relPath,
        abspath: fullPath,
        content,
        meta,
      })
    }
  }

  // If there are both groups and orphan files, wrap files in a "General" group
  if (groups.length > 0 && prompts.length > 0) {
    groups.push({
      id: (parentId + '-general').replace(/[^a-zA-Z0-9-]/g, '-').toLowerCase().replace(/-+/g, '-'),
      label: 'General',
      type: 'group',
      count: prompts.length,
      children: prompts,
    })
    groups.sort((a, b) => a.label.localeCompare(b.label))
    return groups
  }

  // Otherwise return combined (if only files, return as-is)
  const nodes = [...groups, ...prompts]
  nodes.sort((a, b) => {
    if (a.type === 'group' && b.type !== 'group') return -1
    if (a.type !== 'group' && b.type === 'group') return 1
    return a.label.localeCompare(b.label)
  })
  return nodes
}

const folders = ['Agentes', 'Prompts', 'Skills']
const result = {}
for (const f of folders) {
  const dirPath = path.join(ECOSYS, f)
  if (fs.existsSync(dirPath)) {
    result[f] = scanDir(dirPath, f)
  }
}

// Include extra agent files (e.g. ecosys/Agents/) under Agentes as a General group
const extraAgentDir = path.join(ECOSYS, 'Agents')
if (fs.existsSync(extraAgentDir)) {
  const extra = scanDir(extraAgentDir, 'Agentes')
  if (extra.length > 0) {
    result['Agentes'].push({
      id: 'agentes-standalone',
      label: 'Standalone Agents',
      type: 'group',
      count: extra.length,
      children: extra,
    })
  }
}

const json = JSON.stringify(result)
fs.writeFileSync(path.join(__dirname, 'tree-data.json'), JSON.stringify(result, null, 2))
fs.writeFileSync(path.join(__dirname, 'tree-data.js'), 'window.__TREE__ = ' + json + ';')

function countPrompts(nodes) {
  let c = 0
  for (const n of nodes) {
    if (n.type === 'prompt') c++
    if (n.children) c += countPrompts(n.children)
  }
  return c
}

console.log('tree-data.json + tree-data.js regenerated')
for (const f of folders) {
  const items = result[f] || []
  const total = countPrompts(items)
  console.log(`  ${f}: ${items.length} groups, ${total} prompts`)
}
