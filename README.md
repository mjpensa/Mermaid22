# MermaidPaper

Detect & render Mermaid diagrams in PDFs and DOCX files, outputting pixel-matched PDFs.

## Quickstart

### VS Code

1. Open the project in VS Code.
2. Install dependencies: `pip install -r requirements.txt` and `npm install`
3. Run CLI: `python -m app.cli input.pdf -o output.pdf`
4. Run API: `uvicorn app.server:app --reload`

### Dev Containers (optional)

Use VS Code dev containers for isolated environment.

## API Usage

POST /render

- Multipart form with `file` field (PDF or DOCX)
- Returns PDF stream
- Optional ?log=1 for JSON log
- X-MermaidPaper-Log header with JSON

## CLI Usage

python -m app.cli input.pdf -o output.pdf

Flags:
--log-json path
--dpi 300
--max-height-ratio 0.8
--skip-invalid

## Railway Deploy

1. Push to GitHub repo "mermaid2"
2. Connect to Railway
3. Set PORT env var
4. Build command: (default)
5. Start command: uvicorn app.server:app --host 0.0.0.0 --port $PORT

Health: /healthz

## Known Limitations

- Large files >40MB rejected
- Pages >800 capped
- Invalid Mermaid skipped

## Troubleshooting

- Ensure fonts installed
- Check logs for errors