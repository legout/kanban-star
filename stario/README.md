# Stario Kanban Board

Einfaches Kanban-Board implementiert mit [Stario](https://stario.dev/).

## Features

- Drei Spalten: Todo, In Progress, Done
- Tasks hinzufügen
- Tasks zwischen Spalten verschieben
- Tasks löschen
- Reaktive Updates ohne Page Reload
- Server-Sent Events für Echtzeit-Updates

## Installation

```bash
pip install -r requirements.txt
```

## Starten

```bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Die App läuft auf http://localhost:8000
