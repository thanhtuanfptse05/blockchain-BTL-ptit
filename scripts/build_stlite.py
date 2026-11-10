"""Build script to bundle Python source files into a standalone WebAssembly HTML page using stlite.

This enables deploying the Streamlit app directly to GitHub Pages without any Python backend server.
"""

import json
from pathlib import Path


def build() -> None:
    dist_dir = Path("dist")
    dist_dir.mkdir(exist_ok=True)

    src_dir = Path("src")
    files = {}

    for py_file in src_dir.rglob("*.py"):
        rel_path = py_file.as_posix()
        content = py_file.read_text(encoding="utf-8")
        files[rel_path] = content

    requirements = ["pandas", "numpy", "plotly", "pydantic"]

    files_json = json.dumps(files)
    requirements_json = json.dumps(requirements)

    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge" />
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no" />
    <title>DeFi Liquidation Cascade Simulator</title>
    <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.63.1/build/stlite.css" />
    <style>
        body, html {{
            margin: 0;
            padding: 0;
            width: 100%;
            height: 100%;
            background-color: #FFFFFF;
        }}
        #loading-screen {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100vh;
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            color: #0F172A;
            background: #FFFFFF;
        }}
        .spinner {{
            width: 44px;
            height: 44px;
            border: 3px solid #E2E8F0;
            border-top: 3px solid #2563EB;
            border-radius: 50%;
            animation: spin 0.8s linear infinite;
            margin-bottom: 16px;
        }}
        @keyframes spin {{
            0% {{ transform: rotate(0deg); }}
            100% {{ transform: rotate(360deg); }}
        }}
    </style>
</head>
<body>
    <div id="loading-screen">
        <div class="spinner"></div>
        <div style="font-size: 1.15rem; font-weight: 600;">Đang khởi chạy DeFi Liquidation Cascade Simulator...</div>
        <div style="font-size: 0.88rem; color: #64748B; margin-top: 6px;">Đang tải môi trường Python WebAssembly trong trình duyệt...</div>
    </div>
    <div id="root"></div>

    <script src="https://cdn.jsdelivr.net/npm/@stlite/mountable@0.63.1/build/stlite.js"></script>
    <script>
        const files = {files_json};
        const requirements = {requirements_json};

        stlite.mount({{
            requirements: requirements,
            entrypoint: "src/interface/app.py",
            files: files,
            streamlitConfig: {{
                "theme.base": "light",
                "theme.primaryColor": "#2563EB",
                "theme.backgroundColor": "#FFFFFF",
                "theme.secondaryBackgroundColor": "#F8FAFC",
                "theme.textColor": "#0F172A"
            }}
        }}, document.getElementById("root")).then(() => {{
            const loader = document.getElementById("loading-screen");
            if (loader) loader.style.display = "none";
        }});
    </script>
</body>
</html>
"""
    # Write to root index.html so default GitHub Pages branch deployment picks it up immediately
    Path("index.html").write_text(html, encoding="utf-8")
    (dist_dir / "index.html").write_text(html, encoding="utf-8")
    Path(".nojekyll").write_text("", encoding="utf-8")
    (dist_dir / ".nojekyll").write_text("", encoding="utf-8")
    print(f"Build complete: index.html and dist/index.html generated with {len(files)} Python files embedded.")


if __name__ == "__main__":
    build()
