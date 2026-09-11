import os
import json
import random
import itertools

# Rutas base
BASE_DIR = r"C:\Users\djlan\Desktop\Aeperion Aion"
DIRS = {
    "Agentes": ["Frontend_Design", "Backend_Architecture", "DevOps_CI_CD", "Data_Engineering", "QA_Testing", "UX_Research", "Security", "Product_Management"],
    "Skills": ["Interfaces", "Estructuras", "Conectores", "Animaciones", "State_Management", "API_Integration", "Web3", "Performance_Optimization"],
    "Prompts": ["Estructura_DB_Frontend", "Diseño_Formularios_Formspree", "React_Components", "Vue_Directives", "Svelte_Stores", "Tailwind_Styling", "GraphQL_Queries", "Testing_Jest"]
}

# Crear carpetas
for main_dir, sub_dirs in DIRS.items():
    for sub in sub_dirs:
        os.makedirs(os.path.join(BASE_DIR, main_dir, sub), exist_ok=True)

# --- Templates ---
AGENT_TEMPLATE = """# Agente: {name}
**Categoría:** {category}
**Nivel de Autonomía:** Alto

## 1. Descripción General
El agente **{name}** está especializado en tareas de {category}. Su objetivo principal es resolver problemas complejos de manera sistemática y detallada, optimizando el flujo de trabajo en proyectos de gran escala.

## 2. Capacidades Base (Core Capabilities)
- Análisis de requerimientos y diseño de arquitecturas.
- Refactorización y optimización de código legado.
- Generación de documentación técnica detallada.
- Integración continua con otras herramientas del entorno.

## 3. Instrucciones de Sistema (System Prompt)
```text
Actúa como un experto en {category}. 
Tu meta es: {goal}.
Reglas estrictas:
1. Siempre proveer código limpio y comentado.
2. Seguir las mejores prácticas de la industria.
3. Considerar la escalabilidad a largo plazo.
```

## 4. Skills Recomendados (Plugins)
- `File Reader / Writer`
- `Code Execution Sandbox`
- `Web Search (Google / DuckDuckGo)`

## 5. Ejemplos de Uso
**Usuario:** "Necesito optimizar este módulo."
**Agente {name}:** Analiza el contexto, identifica cuellos de botella (ej. renderizados innecesarios, consultas N+1) y propone un plan de acción estructurado con código.
"""

SKILL_TEMPLATE = """# Skill: {name}
**Tipo:** {category}
**Compatibilidad:** Universal (REST, GraphQL, CLI)

## 1. Resumen de la Habilidad
**{name}** proporciona a los agentes la capacidad de interactuar y manipular elementos relacionados con {category}. Esta skill es fundamental para construir sistemas dinámicos y responsivos.

## 2. Casos de Uso (Use Cases)
- Creación rápida de prototipos.
- Migración y transformación de datos.
- Sincronización en tiempo real.
- Mejora de la Experiencia de Usuario (UX).

## 3. Configuración Técnica (Config)
```json
{{
  "skill_id": "{skill_id}",
  "version": "1.0.0",
  "dependencies": ["core-engine", "network-module"],
  "permissions": ["read", "write", "execute"]
}}
```

## 4. Estructura de Entrada/Salida (I/O)
### Input esperado
- `context`: String con el estado actual.
- `parameters`: Objeto JSON con configuración específica.

### Output generado
- `status`: "success" | "error"
- `data`: Resultado procesado de la operación {name}.

## 5. Snippet de Implementación (Python / Node.js)
```javascript
async function execute{function_name}(params) {{
    console.log("Iniciando {name}...");
    // Lógica core para {category}
    return {{ success: true, timestamp: Date.now() }};
}}
```
"""

PROMPT_TEMPLATE = """# Prompt Template: {name}
**Categoría:** {category}
**Nivel de Complejidad:** Avanzado

## 1. Propósito
Este prompt está diseñado para extraer la máxima calidad del LLM cuando se trabaja en tareas relacionadas con **{category}**. Específicamente útil para {name}.

## 2. Estructura del Prompt (The Prompt)
```markdown
Eres un Arquitecto de Software Senior y Diseñador UX.
Tarea actual: {goal}

Contexto:
- El proyecto requiere alta escalabilidad.
- Se debe priorizar la accesibilidad (a11y) y el rendimiento.

Por favor, proporciona:
1. Una explicación paso a paso de tu enfoque.
2. La estructura de carpetas / archivos.
3. El código completo y funcional.
4. Consideraciones de seguridad y rendimiento.
```

## 3. Variables Requeridas
Para usar este prompt efectivamente, asegúrate de reemplazar las siguientes variables en tiempo de ejecución:
- `{{{{project_context}}}}`: Descripción del proyecto.
- `{{{{tech_stack}}}}`: Tecnologías a usar (ej. React, Node, PostgreSQL).
- `{{{{user_requirements}}}}`: Lista de requerimientos específicos del usuario.

## 4. Ejemplo de Respuesta Esperada (Output Mockup)
El modelo debería responder con una estructura de Markdown limpia, empezando por un resumen ejecutivo, seguido de diagramas (Mermaid.js si aplica) y bloques de código con resaltado de sintaxis correcto.
"""

# Datos semilla para la generación procedural
adjectives = ["Advanced", "Dynamic", "Responsive", "Secure", "Scalable", "Intelligent", "Optimized", "Interactive", "Robust", "Agile", "Automated", "Serverless", "Reactive", "Modular"]
nouns = ["System", "Architecture", "Builder", "Generator", "Manager", "Analyzer", "Optimizer", "Connector", "Orchestrator", "Engine", "Processor", "Visualizer", "Integrator"]

# --- Casos Específicos Solicitados ---
specific_files = [
    # Agentes
    ("Agentes", "Frontend_Design", "Agente_Diseño_Frontend_Avanzado.md", AGENT_TEMPLATE.format(name="Frontend Master UX/UI", category="Frontend Design", goal="Crear interfaces pixel-perfect con micro-interacciones avanzadas.")),
    # Skills
    ("Skills", "Interfaces", "Skill_Creacion_Interfaces_Dinamicas.md", SKILL_TEMPLATE.format(name="Dynamic UI Creator", category="Interfaces", skill_id="ui-creator-001", function_name="DynamicUI")),
    ("Skills", "Estructuras", "Skill_Generacion_Estructuras_Datos.md", SKILL_TEMPLATE.format(name="Data Structure Generator", category="Estructuras", skill_id="struct-gen-001", function_name="DataStructure")),
    ("Skills", "Conectores", "Skill_Conectores_API_GraphQL.md", SKILL_TEMPLATE.format(name="GraphQL API Connector", category="Conectores", skill_id="conn-gql-001", function_name="GraphQLConn")),
    ("Skills", "Animaciones", "Skill_Animaciones_FramerMotion.md", SKILL_TEMPLATE.format(name="Framer Motion Animator", category="Animaciones", skill_id="anim-framer-001", function_name="FramerMotion")),
    # Prompts
    ("Prompts", "Estructura_DB_Frontend", "Prompt_Estructura_Base_Datos_Frontend.md", PROMPT_TEMPLATE.format(name="Frontend DB State Architecture", category="Estructura DB Frontend", goal="Diseñar la estructura de estado global (Redux/Zustand) que simula una base de datos relacional en el cliente.")),
    ("Prompts", "Diseño_Formularios_Formspree", "Prompt_Formulario_Diseño_Formspree.md", PROMPT_TEMPLATE.format(name="Formspree Integration & UI", category="Formularios Formspree", goal="Crear un formulario de contacto accesible, estéticamente premium y conectado a Formspree sin backend.")),
]

# Escribir archivos específicos
count = 0
for type_, sub_, filename, content in specific_files:
    filepath = os.path.join(BASE_DIR, type_, sub_, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    count += 1

# Generación Masiva para llegar a >300
# Agentes (aprox 100)
for sub in DIRS["Agentes"]:
    for i in range(13): # 8 sub_dirs * 13 = 104
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        name = f"{adj} {sub.replace('_', ' ')} {noun}"
        filename = f"{name.replace(' ', '_')}_{i}.md"
        filepath = os.path.join(BASE_DIR, "Agentes", sub, filename)
        content = AGENT_TEMPLATE.format(
            name=name, 
            category=sub.replace('_', ' '), 
            goal=f"Optimizar procesos y automatizar tareas complejas dentro del dominio de {sub.replace('_', ' ')}."
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

# Skills (aprox 104)
for sub in DIRS["Skills"]:
    for i in range(13):
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        name = f"{adj} {sub.replace('_', ' ')} {noun}"
        filename = f"{name.replace(' ', '_')}_{i}.md"
        filepath = os.path.join(BASE_DIR, "Skills", sub, filename)
        content = SKILL_TEMPLATE.format(
            name=name, 
            category=sub.replace('_', ' '),
            skill_id=f"{sub.lower()}-{i:03d}",
            function_name=name.replace(' ', '')
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

# Prompts (aprox 104)
for sub in DIRS["Prompts"]:
    for i in range(13):
        adj = random.choice(adjectives)
        noun = random.choice(nouns)
        name = f"{adj} {sub.replace('_', ' ')} {noun}"
        filename = f"{name.replace(' ', '_')}_{i}.md"
        filepath = os.path.join(BASE_DIR, "Prompts", sub, filename)
        content = PROMPT_TEMPLATE.format(
            name=name, 
            category=sub.replace('_', ' '),
            goal=f"Generar código y estrategias óptimas para resolver requerimientos de {sub.replace('_', ' ')} utilizando técnicas de vanguardia."
        )
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        count += 1

print(f"Éxito: Se generaron {count} archivos Markdown distribuidos en Agentes, Skills y Prompts.")
