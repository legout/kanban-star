# Kanban Board Vergleich

Dieses Repository enthält zwei identische Kanban-Board-Implementierungen:
- **StarHTML** - Python-first Hypermedia Framework
- **Stario** - Auf Starlette basierendes Real-time Framework

Beide nutzen [Datastar](https://data-star.dev/) für reaktive Frontend-Updates.

## 📁 Struktur

```
.
├── starhtml/           # StarHTML Implementierung
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── stario/             # Stario Implementierung
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── render.yaml         # Render Deployment Konfiguration
└── README.md           # Diese Datei
```

## 🚀 Deployment

### Option 1: Render (Empfohlen, Kostenlos)

1. Fork dieses Repository
2. Erstelle ein kostenloses Konto auf [Render](https://render.com)
3. Klicke "New +" → "Blueprint"
4. Verbinde dein GitHub Repo
5. Render erstellt automatisch beide Services

Die Apps sind dann verfügbar unter:
- StarHTML: `https://kanban-starhtml-xxx.onrender.com`
- Stario: `https://kanban-stario-xxx.onrender.com`

### Option 2: Lokal testen

**StarHTML:**
```bash
cd starhtml
pip install -r requirements.txt
python app.py
# Öffne http://localhost:5001
```

**Stario:**
```bash
cd stario
pip install -r requirements.txt
uvicorn app:app --reload
# Öffne http://localhost:8000
```

## 📊 Vergleich

Siehe [kanban_comparison.md](./kanban_comparison.md) für eine detaillierte Bewertung.

| Kriterium | StarHTML | Stario |
|-----------|----------|--------|
| Einfachheit | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Eleganz | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| Robustheit | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Echtzeit | Gut | Hervorragend |

## 📝 Lizenz

MIT
