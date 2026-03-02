"""
Stario Kanban Board - vereinfachte Version für Stario v2
"""

from stario import Stario

app = Stario(tracer=None)

# In-Memory Task-Storage (für Demo)
tasks_db = {
    "todo": ["Task 1", "Task 2"],
    "inprogress": ["Task 3"],
    "done": []
}

COLUMNS = [
    ("todo", "📋 Todo"),
    ("inprogress", "🔄 In Progress"),
    ("done", "✅ Done")
]


def render_board():
    """Das komplette Kanban-Board als HTML rendern"""
    columns_html = ""
    
    for col_id, title in COLUMNS:
        col_ids = [c[0] for c in COLUMNS]
        current_idx = col_ids.index(col_id)
        next_col = col_ids[current_idx + 1] if current_idx < len(col_ids) - 1 else None
        prev_col = col_ids[current_idx - 1] if current_idx > 0 else None
        
        tasks_html = ""
        for task in tasks_db[col_id]:
            buttons = ""
            
            if prev_col:
                buttons += f'''<button data-on:click="@post('/move/{task}/{col_id}/{prev_col}')" style="margin-right: 5px;">←</button>'''
            
            buttons += f'''<button data-on:click="@post('/delete/{task}/{col_id}')" style="margin-right: 5px;">🗑️</button>'''
            
            if next_col:
                buttons += f'''<button data-on:click="@post('/move/{task}/{col_id}/{next_col}')">→</button>'''
            
            tasks_html += f'''
            <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: white; display: flex; justify-content: space-between; align-items: center; border-radius: 4px;">
                <span style="flex: 1;">{task}</span>
                <div style="display: flex; gap: 5px;">{buttons}</div>
            </div>
            '''
        
        columns_html += f'''
        <div style="flex: 1; margin: 0 10px; background: #e9ecef; padding: 15px; border-radius: 8px; min-width: 250px;">
            <h3 style="margin-top: 0; color: #333;">{title}</h3>
            <div style="min-height: 300px; background: #f8f9fa; padding: 10px; border-radius: 4px;">
                {tasks_html}
            </div>
        </div>
        '''
    
    return columns_html


def homepage():
    """Hauptseite mit Kanban-Board"""
    board_html = render_board()
    
    return f'''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Kanban Board - Stario</title>
        <script type="module" src="https://cdn.jsdelivr.net/npm/@starfederation/datastar@1.0.0-beta.9/dist/datastar.min.js"></script>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; margin: 0; padding: 20px; }}
            .container {{ max-width: 1400px; margin: 0 auto; }}
            h1 {{ text-align: center; color: #2c3e50; }}
            .subtitle {{ text-align: center; color: #666; margin-bottom: 30px; }}
            .input-area {{ text-align: center; margin-bottom: 30px; }}
            input {{ padding: 10px; font-size: 16px; width: 300px; border: 1px solid #ddd; border-radius: 4px; }}
            button.add {{ padding: 10px 20px; font-size: 16px; margin-left: 10px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer; }}
            .board {{ display: flex; justify-content: center; gap: 10px; flex-wrap: wrap; }}
            .notification {{ text-align: center; margin-bottom: 20px; padding: 10px; border-radius: 4px; }}
            .success {{ color: green; background: #d4edda; }}
            .info {{ color: #3498db; background: #d1ecf1; }}
            .error {{ color: #e74c3c; background: #f8d7da; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>📝 Kanban Board - Stario</h1>
            <p class="subtitle">Built with Stario v2 + Datastar</p>
            
            <div class="input-area">
                <input data-bind="new_task" placeholder="Neue Task eingeben..." />
                <button class="add" data-on:click="@post('/add_task')">➕ Hinzufügen</button>
            </div>
            
            <div id="notification"></div>
            
            <div id="board" class="board">
                {board_html}
            </div>
        </div>
    </body>
    </html>
    '''


# Routes registrieren
app.get("/", homepage)


def add_task(new_task: str):
    """Neue Task zu Todo hinzufügen"""
    if new_task and new_task.strip():
        tasks_db["todo"].append(new_task.strip())
    
    board_html = render_board()
    
    return f'''
    <div id="notification" class="notification success">✅ Task '{new_task}' hinzugefügt!</div>
    <div id="board" class="board">{board_html}</div>
    '''


app.post("/add_task", add_task)


def move_task(task: str, from_col: str, to_col: str):
    """Task zwischen Spalten verschieben"""
    if task in tasks_db.get(from_col, []):
        tasks_db[from_col].remove(task)
        tasks_db[to_col].append(task)
    
    board_html = render_board()
    
    return f'''
    <div id="notification" class="notification info">📍 {task} verschoben!</div>
    <div id="board" class="board">{board_html}</div>
    '''


app.post("/move/{task}/{from_col}/{to_col}", move_task)


def delete_task(task: str, col: str):
    """Task löschen"""
    if task in tasks_db.get(col, []):
        tasks_db[col].remove(task)
    
    board_html = render_board()
    
    return f'''
    <div id="notification" class="notification error">🗑️ {task} gelöscht!</div>
    <div id="board" class="board">{board_html}</div>
    '''


app.post("/delete/{task}/{col}", delete_task)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
