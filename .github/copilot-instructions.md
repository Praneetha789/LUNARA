## Repository quick summary

This repo is a small desktop-style assistant built with a Python backend and a browser-based frontend served via Eel.

High level:
- Python process (entry: `main.py`) initializes Eel with the `www/` folder and starts the UI (`www/index.html`).
- Backend code lives under `engine/` (look for `engine/command.py`, `engine/config.py`, `engine/...`).
- Frontend static files live in `www/` (entrypoint `www/index.html`, scripts `main.js`, `controller.js`, assets under `www/assets/`).
- SQLite DB `LUNARA.db` (repo root) holds mappings the assistant uses (example tables: `sys_command`, `web_command`).

## How the app runs (use these exact commands on Windows PowerShell)

1) Activate the bundled virtualenv:

```powershell
.\envLUNARA\Scripts\Activate.ps1
```

2) Start the app from the repo root:

```powershell
python main.py
```

Notes: `main.py` calls `eel.init('www')` then `eel.start('index.html', host='localhost', block=True)`. It also starts Chrome with a Windows `start chrome.exe` command (so the project expects Chrome on Windows).

## Key files and responsibilities (pick these when editing or answering questions)
- `main.py` — startup: initializes Eel, plays startup sound and opens the browser app.
- `engine/engine/www/www/features.py` — backend endpoints exposed to the frontend (`@eel.expose`), DB access (`sqlite3.connect('LUNARA.db')`), audio helpers (`playsound`) and helpers like `openCommand()` and `PlayYoutube()` used by the assistant.
- `engine/command.py` — speech / assistant commands (imported by `features.py`) — check here for `speak()` implementation and other core behaviors.
- `engine/config.py` — small constants (for example `ASSISTANT_NAME`) used across code.
- `LUNARA.db` — contains `sys_command` and `web_command` tables used by `openCommand()` to map names to system paths or URLs.
- `www/index.html`, `www/main.js`, `www/controller.js` — frontend UI and event wiring. The frontend loads `/eel.js` and calls Python-exposed functions.
- `www/assets/audio/` — audio files used by `playAssistantSound()` and `playClickSound()`.

## Important integration points & patterns for AI edits
- Eel bridging: Python functions intended for JS must be decorated with `@eel.expose` and callable from the JS side. When changing an exposed function, update both the Python and JS call sites (search for `eel.expose` and `/eel.js` usage).
- SQLite usage: `features.py` queries use `LOWER(name) = ?` to normalize lookups. When adding commands to `sys_command` or `web_command`, ensure names are stored in a way that matches these queries.
- OS calls: `openCommand()` sometimes calls `os.startfile()` or `os.system('start ...')` — these are Windows-specific. Keep that in mind when adding cross-platform code.
- External libs observed: `eel`, `playsound`, `pywhatkit`, `pywhatkit.playonyt()`. Changes touching these should consider blocking behavior and long-running calls.

## Debug / dev tips (practical, repo-specific)
- If the UI doesn't load, run `python main.py` and inspect the terminal for Eel errors. Because `eel.start(..., block=True)` blocks, you will see backend logs in the same terminal.
- To quickly test an exposed function, run `python -c "import engine.engine.www.www.features as f; print(f.extract_yt_term('play blinding lights on youtube'))"` adjusting the import path as needed (the project has a nested `engine/engine/www/www/` layout).
- When editing DB-driven commands, open `LUNARA.db` with any SQLite viewer and inspect `sys_command` / `web_command` entries used by `openCommand()`.

## Patterns and gotchas discovered
- The repo uses a nested folder layout (`engine/engine/www/www/`) — file paths are relative and a little duplicated; be careful when editing imports or moving files.
- Audio playback is synchronous (uses `playsound`) — long audio will block the Python process. Consider using threads or non-blocking playback if you modify behavior.
- The startup uses `os.system('start chrome.exe --app="http://localhost:8000/index.html"')` in `main.py` — Chrome is assumed and the port/URL may not match Eel's final host/port. Prefer relying on `eel.start()` to open the browser, or update the command if you change `eel.start()` options.

## Example snippets the agent can reference
- How `openCommand()` looks up a system app:

```
cursor.execute('SELECT path FROM sys_command WHERE LOWER(name) = ?', (query,))
if results:
    os.startfile(results[0][0])
```

- How the frontend triggers a backend play-click-sound action:

```
@eel.expose
def playClickSound():
    playsound('www\\assets\\audio\\click_sound.mp3')
```

## If you need to change dev setup
- There is no `requirements.txt` in the repo root. The project includes a virtualenv (`envLUNARA`) containing installed packages. If you add or change dependencies, update a `requirements.txt` and document installation steps.

---
Please review this file and tell me any areas you want expanded (examples of JS <> Python flows, more DB table references, or adding a small run script). I'll iterate based on your feedback.
