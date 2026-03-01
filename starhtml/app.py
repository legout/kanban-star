from starhtml import *

app, rt = star_app()

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
    tasks_html = []
    
    col_ids = [c[0] for c in COLUMNS]
    current_idx = col_ids.index(column_id)
    next_col = col_ids[current_idx + 1] if current_idx < len(col_ids) - 1 else None
    
    for task in tasks:
        buttons = []
        # Move Left Button
        if current_idx > 0:
            prev_col = col_ids[current_idx - 1]
            buttons.append(
                Button(
                    "←",
                    data_on_click=post(f"/move/{column_id}/{prev_col}", {"task": task}),
                    style="margin-right: 5px;"
                )
            )
        # Delete Button
        buttons.append(
            Button(
                "🗑️",
                data_on_click=post(f"/delete/{column_id}", {"task": task}),
                style="margin-right: 5px;"
            )
        )
        # Move Right Button
        if next_col:
            buttons.append(
                Button(
                    "→",
                    data_on_click=post(f"/move/{column_id}/{next_col}", {"task": task})
                )
            )
        
        tasks_html.append(
            Div(
                Span(task, style="flex: 1;"),
                Div(*buttons, style="display: flex; gap: 5px;"),
                style="border: 1px solid #ddd; padding: 10px; margin: 5px 0; background: white; display: flex; justify-content: space-between; align-items: center; border-radius: 4px;"
            )
        )
    
    return Div(
        H3(title, style="margin-top: 0; color: #333;"),
        Div(
            *tasks_html,
            style="min-height: 300px; background: #f8f9fa; padding: 10px; border-radius: 4px;"
        ),
        style="flex: 1; margin: 0 10px; background: #e9ecef; padding: 15px; border-radius: 8px; min-width: 250px;"
    )


@rt('/')
def home():
    # Signale für das Formular
    (new_task := Signal("new_task", ""))
    
    return Div(
        # Header
        H1("📝 Kanban Board - StarHTML", style="text-align: center; color: #2c3e50;"),
        P("Built with StarHTML + Datastar", style="text-align: center; color: #666; margin-bottom: 30px;"),
        
        # Neue Task eingeben
        Div(
            Input(
                placeholder="Neue Task eingeben...",
                data_bind=new_task,
                style="padding: 10px; font-size: 16px; width: 300px; border: 1px solid #ddd; border-radius: 4px;"
            ),
            Button(
                "➕ Hinzufügen",
                data_on_click=post("/add_task", {"task": new_task}),
                style="padding: 10px 20px; font-size: 16px; margin-left: 10px; background: #3498db; color: white; border: none; border-radius: 4px; cursor: pointer;"
            ),
            style="text-align: center; margin-bottom: 30px;"
        ),
        
        # Notification-Bereich
        Div(id="notification"),
        
        # Kanban-Board
        Div(
            kanban_column("todo", "📋 Todo", tasks_db["todo"]),
            kanban_column("inprogress", "🔄 In Progress", tasks_db["inprogress"]),
            kanban_column("done", "✅ Done", tasks_db["done"]),
            style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;"
        ),
        
        style="max-width: 1400px; margin: 0 auto; padding: 20px; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; background: #f5f5f5; min-height: 100vh;"
    )


@rt('/add_task')
def add_task(task: str):
    """Neue Task zu Todo hinzufügen"""
    if task and task.strip():
        tasks_db["todo"].append(task.strip())
    
    # Aktualisiertes Board zurückgeben
    return Div(
        # Notification
        Div(
            f"✅ Task '{task}' hinzugefügt!",
            style="color: green; text-align: center; margin-bottom: 20px; padding: 10px; background: #d4edda; border-radius: 4px;",
            id="notification"
        ),
        # Aktualisiertes Board
        Div(
            kanban_column("todo", "📋 Todo", tasks_db["todo"]),
            kanban_column("inprogress", "🔄 In Progress", tasks_db["inprogress"]),
            kanban_column("done", "✅ Done", tasks_db["done"]),
            style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;",
            id="board"
        )
    )


@rt('/move/{from_col}/{to_col}')
def move_task(from_col: str, to_col: str, task: str):
    """Task zwischen Spalten verschieben"""
    if task in tasks_db.get(from_col, []):
        tasks_db[from_col].remove(task)
        tasks_db[to_col].append(task)
    
    return Div(
        Div(
            f"📍 {task} verschoben!",
            style="color: #3498db; text-align: center; margin-bottom: 20px; padding: 10px; background: #d1ecf1; border-radius: 4px;",
            id="notification"
        ),
        Div(
            kanban_column("todo", "📋 Todo", tasks_db["todo"]),
            kanban_column("inprogress", "🔄 In Progress", tasks_db["inprogress"]),
            kanban_column("done", "✅ Done", tasks_db["done"]),
            style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;",
            id="board"
        )
    )


@rt('/delete/{col}')
def delete_task(col: str, task: str):
    """Task löschen"""
    if task in tasks_db.get(col, []):
        tasks_db[col].remove(task)
    
    return Div(
        Div(
            f"🗑️ {task} gelöscht!",
            style="color: #e74c3c; text-align: center; margin-bottom: 20px; padding: 10px; background: #f8d7da; border-radius: 4px;",
            id="notification"
        ),
        Div(
            kanban_column("todo", "📋 Todo", tasks_db["todo"]),
            kanban_column("inprogress", "🔄 In Progress", tasks_db["inprogress"]),
            kanban_column("done", "✅ Done", tasks_db["done"]),
            style="display: flex; justify-content: center; gap: 10px; flex-wrap: wrap;",
            id="board"
        )
    )


if __name__ == "__main__":
    serve()
