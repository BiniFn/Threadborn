from pathlib import Path

api_dir = Path("api")
function_files = sorted(
    path
    for path in api_dir.rglob("*.js")
    if not path.name.startswith("_")
)

if function_files != [api_dir / "index.js"]:
    found = "\n".join(str(path) for path in function_files)
    raise SystemExit(
        "Threadborn API is expected to use one function file: api/index.js\n"
        f"Found:\n{found}"
    )

print("Threadborn API is already combined into api/index.js.")
