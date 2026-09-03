from __future__ import annotations

import json
import sys
from http.server import BaseHTTPRequestHandler
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from rag_project.classifier import classify_application
from rag_project.pipeline import RagPipeline


PIPELINE = RagPipeline.from_documents(PROJECT_ROOT / "data" / "red_cross_examples")


HTML = """<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Red Cross RAG Demo</title>
  <style>
    :root { color-scheme: dark; font-family: Inter, system-ui, sans-serif; }
    body { margin: 0; background: #101614; color: #edf4ef; }
    main { max-width: 980px; margin: 0 auto; padding: 48px 20px; }
    h1 { margin-bottom: 8px; font-size: clamp(2rem, 5vw, 4rem); }
    p { color: #b7c8bd; line-height: 1.6; }
    .panel { border: 1px solid #304139; background: #17211c; padding: 24px; margin-top: 24px; }
    textarea { width: 100%; min-height: 110px; box-sizing: border-box; background: #0d1210; color: #edf4ef; border: 1px solid #52675a; padding: 14px; font: inherit; }
    button { margin-top: 14px; background: #e0f1e4; color: #132219; border: 0; padding: 12px 18px; font: inherit; font-weight: 700; cursor: pointer; }
    button:disabled { opacity: .6; cursor: wait; }
    pre { white-space: pre-wrap; color: #dbeade; line-height: 1.55; }
    .label { color: #8fc29b; text-transform: uppercase; letter-spacing: .08em; font-size: .75rem; font-weight: 700; }
    #status { min-height: 1.5em; }
  </style>
</head>
<body>
  <main>
    <div class="label">Swedish Red Cross internship prototype</div>
    <h1>RAG-assisted application analysis</h1>
    <p>Ask a question about the synthetic application examples. The system retrieves source passages, produces an answer, and returns citations.</p>
    <section class="panel">
      <textarea id="question">How can previous applications be classified to support future reports?</textarea>
      <button id="ask">Ask the RAG assistant</button>
      <p id="status"></p>
      <pre id="answer"></pre>
    </section>
    <section class="panel">
      <div class="label">Application classification</div>
      <pre id="classification">Run a question to see the structured classification.</pre>
    </section>
  </main>
  <script>
    const question = document.querySelector('#question');
    const button = document.querySelector('#ask');
    const status = document.querySelector('#status');
    const answer = document.querySelector('#answer');
    const classification = document.querySelector('#classification');
    button.onclick = async () => {
      button.disabled = true;
      status.textContent = 'Retrieving sources...';
      try {
        const response = await fetch('/api', { method: 'POST', headers: {'Content-Type': 'application/json'}, body: JSON.stringify({question: question.value}) });
        const data = await response.json();
        if (!response.ok) throw new Error(data.error || 'Request failed');
        answer.textContent = data.answer + '\\n\\nSources:\\n' + data.citations.join('\\n');
        classification.textContent = JSON.stringify(data.classification, null, 2);
        status.textContent = 'Complete';
      } catch (error) { status.textContent = error.message; }
      button.disabled = false;
    };
  </script>
</body>
</html>"""


class handler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        self._send(200, HTML, "text/html; charset=utf-8")

    def do_POST(self) -> None:
        try:
            size = int(self.headers.get("Content-Length", "0"))
            payload = json.loads(self.rfile.read(size) or b"{}")
            question = str(payload.get("question", "")).strip()
            if not question:
                raise ValueError("question is required")
            result = PIPELINE.ask(question, top_k=3)
            application_text = "\n".join(document.text for document in PIPELINE_DOCUMENTS)
            classification = classify_application(application_text)
            body = json.dumps({
                "answer": result.answer,
                "citations": result.citations,
                "classification": classification.__dict__,
            })
            self._send(200, body, "application/json; charset=utf-8")
        except (ValueError, json.JSONDecodeError) as exc:
            self._send(400, json.dumps({"error": str(exc)}), "application/json; charset=utf-8")

    def _send(self, status: int, body: str, content_type: str) -> None:
        encoded = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(encoded)))
        self.end_headers()
        self.wfile.write(encoded)


from rag_project.loaders import load_markdown_documents

PIPELINE_DOCUMENTS = load_markdown_documents(PROJECT_ROOT / "data" / "red_cross_examples")
