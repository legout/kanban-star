import asyncio
from stario import Stario
from stario.html import div, h1, h3, input_, button, span, p
from stario.toys import toy_page

app = Stario()

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


def kanban_column(column_id: str, title: str, tasks: list):
    """Eine Kanban-Spalte rendern"""
    tasks_html = ""
    
    col_ids = [c[0] for c in COLUMNS]
    current_idx = col_ids.index(column_id)
    next_col = col_ids[current_idx + 1] if current_idx < len(col_ids) - 1 else None
    prev_col = col_ids[current_idx - 1] if current_idx > 0 else None
    
    for task in tasks:
        buttons = ""
        
        # Move Left Button
        if prev_col:
            buttons += f'''<button data-on:click="@post('/move/{task}/{column_id}/{prev_col}')" style="margin-right: 5px;">←</button>'''
        
        # Delete Button
        buttons += f'''<button data-on:click="@post('/delete/{task}/{column_id}')" style="margin-right: 5px;">🗑️</button>'''
        
        # Move Right Button
        if next_col:
            buttons += f'''<button data-on:click="@post('/move/{task}/{column_id}/{next_col}')">→</button>'''
        
        tasks_html += f'''
        <div style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: white; display: flex; justify-content: space-between; align-items: center; border-radius: 4px;">
            <span style="flex: 1;">{task}</span>
            <div style="display: flex; gap: 5px;">{buttons}</div>
        </div>
        '''
    
    return f'''
    <div style="flex: 1; margin: 0 10px; background: #e9ecef; padding: 15px; border-radius: 8px; min-width: 250px;">
        <h3 style="margin-top: 0; color: #333;">{title}</h3>
        <div style="min-height: 300px; background: #f8f9fa; padding: 10px; border-radius: 4px;">
            {tasks_html}
        </div>
    </div>
    '''


@app.query("/")
async def homepage():
    """Hauptseite mit Kanban-Board"""
    columns_html = ""
    for col_id, title in COLUMNS:
        columns_html += kanban_column(col_id, title, tasks_db[col_id])
    
    return toy_page(
        # Header
        h1("📝 Kanban Board - Stario", style="text-align: center; color: #2c3e50;"),
        p("Built with Stario + Datastar + Starlette", style="text-align: center; color: #666; margin-bottom: 30px;"),
        
        # Neue Task eingeben
        div(
            input_(
                {"data-bind": "new_task"},
                {
                    "placeholder": "Neue Task eingeben...",
                    "style": "padding: 10px; font-size: 16px; width: 300px; border: 1px solid #ddd; border-radius: 4px;"
                }
            ),
            button(
                {"data-on:click": "@post('/add_task')", "style": "padding: 10px 20px; font-size: 16px; margin-left: 10px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;"},
                "➕ Hinzufügen"
            ),
            {"style": "text-align: center; margin-bottom: 30px;"}
        ),
        
        # Notification-Bereich
        div({"id": "notification"}),
        
        # Kanban-Spalten
        div(
            columns_html,
            {"style": "display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;", "id": "board"}
        ),
        
        # Styling
        {"style": "max-width: 1400px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; min-height: 100vh;"}
    )


@app.command("/add_task")
async def add_task(new_task: str):
    """Neue Task zu Todo hinzufügen"""
    if new_task and new_task.strip():
        tasks_db["todo"].append(new_task.strip())
    
    # Board neu rendern
    columns_html = ""
    for col_id, title in COLUMNS:
        columns_html += kanban_column(col_id, title, tasks_db[col_id])
    
    return div(
        # Notification
        div(
            f"✅ Task '{new_task}' hinzugefügt!",
            {"style": "color: green; text-align: center; margin-bottom: 20px; padding: 10px; background: #d4edda; border-radius: 4px;"}
        ),
        # Aktualisiertes Board
        div(
            columns_html,
            {"style": "display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;"}
        ),
        {"id": "board"}
    )


@app.command("/move/{task}/{from_col}/{to_col}")
async def move_task(task: str, from_col: str, to_col: str):
    """Task zwischen Spalten verschieben"""
    if task in tasks_db.get(from_col, []):
        tasks_db[from_col].remove(task)
        tasks_db[to_col].append(task)
    
    # Board neu rendern
    columns_html = ""
    for col_id, title in COLUMNS:
        columns_html += kanban_column(col_id, title, tasks_db[col_id])
    
    return div(
        # Notification
        div(
            f"📍 {task} verschoben!",
            {"style": "color: #3498db; text-align: center; margin-bottom: 20px; padding: 10px; background: #d1ecf1; border-radius: 4px;"}
        ),
        # Aktualisiertes Board
        div(
            columns_html,
            {"style": "display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;"}
        ),
        {"id": "board"}
    )


@app.command("/delete/{task}/{col}")
async def delete_task(task: str, col: str):
    """Task löschen"""
    if task in tasks_db.get(col, []):
        tasks_db[col].remove(task)
    
    # Board neu rendern
    columns_html = ""
    for col_id, title in COLUMNS:
        columns_html += kanban_column(col_id, title, tasks_db[col_id])
    
    return div(
        # Notification
        div(
            f"🗑️ {task} gelöscht!",
            {"style": "color: #e74c3c; text-align: center; margin-bottom: 20px; padding: 10px; background: #f8d7da; border-radius: 4px;"}
        ),
        # Aktualisiertes Board
        div(
            columns_html,
            {"style": "display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;"}
        ),
        {"id": "board"}
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
