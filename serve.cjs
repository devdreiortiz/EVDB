const http = require('http')
const fs = require('fs')
const path = require('path')

const PORT = 5173
const PUBLIC = __dirname

const MIME = {
  '.html': 'text/html',
  '.css': 'text/css',
  '.js': 'text/javascript',
  '.json': 'application/json',
  '.png': 'image/png',
  '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml',
  '.txt': 'text/plain',
  '.md': 'text/markdown',
}

http.createServer((req, res) => {
  let url = req.url.split('?')[0]

  if (url === '/api/tree') {
    const p = path.join(PUBLIC, 'tree-data.json')
    if (fs.existsSync(p)) {
      const data = fs.readFileSync(p, 'utf-8')
      res.writeHead(200, {
        'Content-Type': 'application/json',
        'Access-Control-Allow-Origin': '*',
      })
      res.end(data)
      return
    }
    res.writeHead(404)
    res.end('{}')
    return
  }

  const safe = path.normalize(url).replace(/^(\.\.[/\\])+/, '')
  let filePath = path.join(PUBLIC, safe === '/' ? 'index.html' : safe)

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' })
      res.end('404 Not Found')
      return
    }
    const ext = path.extname(filePath)
    res.writeHead(200, { 'Content-Type': MIME[ext] || 'application/octet-stream' })
    res.end(data)
  })
}).listen(PORT, () => {
  console.log(`\n  Aeperion EVDB`)
  console.log(`  http://localhost:${PORT}\n`)
})
