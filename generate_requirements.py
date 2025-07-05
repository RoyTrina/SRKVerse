import ast
import os
import pkg_resources
import sys

# Path to your source code
PROJECT_DIR = "app"

# Keywords to detect dev tools
DEV_KEYWORDS = ["pytest", "black", "flake8", "mypy", "isort", "pre-commit", "coverage", "tox"]

# Add known built-in Python modules to ignore
def get_stdlib_modules():
    try:
        return sys.stdlib_module_names  # Python 3.10+
    except AttributeError:
        return {
            'os', 'sys', 'json', 're', 'math', 'time', 'random', 'datetime', 'pathlib',
            'typing', 'subprocess', 'logging', 'threading', 'http', 'urllib', 'email', 'itertools',
        }

# Step 1: Extract all import statements from codebase
def find_imports(directory):
    packages = set()
    for [root, _, files] in os.walk(directory):
        for filename in files:
            if filename.endswith(".py"):
                full_path = os.path.join(root, filename)
                try:
                    with open(full_path, "r", encoding="utf-8") as file:
                        tree = ast.parse(file.read())
                        for node in ast.walk(tree):
                            if isinstance(node, ast.Import):
                                for n in node.names:
                                    packages.add(n.name.split('.')[0])
                            elif isinstance(node, ast.ImportFrom):
                                if node.module:
                                    packages.add(node.module.split('.')[0])
                except SyntaxError:
                    print(f"⚠️ Skipping file with syntax error: {full_path}")
    return packages

# Step 2: Classify used imports into runtime and dev requirements
def classify_packages(imports):
    stdlib = get_stdlib_modules()
    installed = {pkg.key: pkg.version for pkg in pkg_resources.working_set}
    run_time = set()
    dev = set()

    for imp in imports:
        name = imp.lower()
        if name in stdlib:
            continue
        if name in installed:
            versioned = f"{name}=={installed[name]}"
            if any(dev_kw in name for dev_kw in DEV_KEYWORDS):
                dev.add(versioned)
            else:
                run_time.add(versioned)
    return run_time, dev

# Step 3: Write a requirements.txt file
def write_requirements(packages, filename):
    with open(filename, "w") as f:
        for pkg in sorted(packages):
            f.write(pkg + "\n")
    print(f"📦 {filename} created ({len(packages)} packages).")

if __name__ == "__main__":
    print("🔍 Scanning Python files in project...")
    imports = find_imports(PROJECT_DIR)

    print("📦 Classifying into user and developer dependencies...")
    runtime, dev = classify_packages(imports)

    write_requirements(runtime, "requirements.txt")
    write_requirements(dev, "dev-requirements.txt")