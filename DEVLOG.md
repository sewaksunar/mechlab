Perfect 👍
Below is a **complete, clean, copy-paste ready `DEVLOG.md`** written in **proper Markdown**, covering **everything step-by-step**: setup, docs, GitHub Pages, and PyPI publishing.

You can save this **exactly as `DEVLOG.md`** in your repo root.

---

# MechLab – Development & Deployment Log (DEVLOG)

This document records the **complete setup, documentation, GitHub Pages deployment, and PyPI publishing workflow** for the `mechlab` Python library.

It is intended to be reusable for **future releases**.

---

## Project Information

- **Package name:** mechlab
- **Current version:** 0.1.1
- **Description:** Computational Mechanical Engineering Toolkit
- **Author:** Sewak Sunar
- **License:** MIT
- **Build system:** Poetry (PEP 621)
- **Documentation:** Sphinx
- **Hosting:** GitHub Pages
- **Distribution:** PyPI

---

## 1. Environment Setup

### Python
- Python **>= 3.14**

### Poetry
Install Poetry:
```bash
pip install poetry
````

Enable in-project virtual environment:

```bash
poetry config virtualenvs.in-project true
```

Install dependencies:

```bash
poetry install
```

Activate environment (Poetry 2.x):

```bash
poetry env activate
```

> Note: `poetry shell` is deprecated in Poetry ≥ 2.0

---

## 2. Project Structure

```text
mechlab/
├── mechlab/              # Python package
├── docs/                 # Sphinx documentation
│   ├── source/
│   └── build/
├── pyproject.toml
├── poetry.lock
├── README.md
├── LICENSE
└── DEVLOG.md
```

---

## 3. Documentation (Sphinx)

### Install documentation dependencies

```bash
poetry add --group docs sphinx furo myst-parser sphinx-design sphinx-copybutton
```

---

### Generate API documentation

```bash
poetry run sphinx-apidoc -o docs/source mechlab
```

This generates:

* `modules.rst`
* module documentation files

---

### Build HTML documentation

```bash
poetry run sphinx-build -b html docs/source docs/build
```

Output:

```text
docs/build/index.html
```

---

### View documentation locally

Open in browser:

```text
docs/build/index.html
```

---

## 4. Common Sphinx Fixes

### Fix: Title underline too short

```rst
MechLab Documentation
====================
```

Underline must match title length.

---

### Fix: toctree document has no title

Every `.rst` file **must start with a title**.

```rst
Thermodynamics
==============

.. automodule:: mechlab.thermodynamics
   :members:
```

---

### Fix: ModuleNotFoundError in autodoc

Add to `docs/source/conf.py`:

```python
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
```

---

## 5. GitHub Pages Deployment (Sphinx)

### Create gh-pages branch

```bash
git branch gh-pages
```

---

### Create Git worktree

```bash
git worktree add ../mechlab-docs gh-pages
```

Directory layout:

```text
MechLab/
├── mechlab/        # main branch
└── mechlab-docs/   # gh-pages branch
```

---

### Copy built docs

```bash
Copy-Item docs\build\* ..\mechlab-docs\ -Recurse -Force
```

---

### Disable Jekyll

```bash
cd ../mechlab-docs
New-Item .nojekyll -Force
```

---

### Commit & push docs

```bash
git add .
git commit -m "Deploy documentation"
git push origin gh-pages
```

---

### Enable GitHub Pages

GitHub → **Settings → Pages**

* Source: Deploy from branch
* Branch: `gh-pages`
* Folder: `/ (root)`

Documentation URL:

```
https://sewaksunar.github.io/mechlab/
```

---

## 6. PyPI Packaging (Poetry)

### Build package

```bash
poetry build
```

Artifacts:

```text
dist/
├── mechlab-0.1.1.tar.gz
└── mechlab-0.1.1-py3-none-any.whl
```

---

## 7. PyPI Metadata Fixes

### Invalid classifier (removed)

```text
Topic :: Scientific/Engineering :: Mechanical Engineering
```

❌ Not a valid PyPI classifier

---

### Valid classifiers used

```toml
classifiers = [
  "Development Status :: 3 - Alpha",
  "Intended Audience :: Science/Research",
  "Intended Audience :: Education",
  "Topic :: Scientific/Engineering",
  "Topic :: Scientific/Engineering :: Physics",
  "License :: OSI Approved :: MIT License",
  "Programming Language :: Python :: 3",
  "Operating System :: OS Independent"
]
```

---

### License fix

```toml
license = "MIT"
```

---

### Scripts fix

```toml
[project.scripts]
dev = "scripts:docs_dev"
```

---

### Update lock file

```bash
poetry lock
```

---

### Validate package

```bash
poetry check
```

---

### Publish to PyPI

```bash
poetry publish
```

Or build + publish:

```bash
poetry publish --build
```

---

## 8. Release Checklist

* [x] Docs build successfully
* [x] Docs render locally
* [x] GitHub Pages live
* [x] Valid PyPI classifiers
* [x] Poetry check passes
* [x] Wheel & sdist built
* [x] PyPI upload successful

---

## 9. Future Improvements

* Versioned documentation (`/v0.2/`)
* Read the Docs integration
* GitHub Actions CI/CD
* Automated PyPI releases
* Example gallery
* API stability guarantees

---

## End of DEVLOG

```

---

If you want next, I can:
- 🔁 automate **docs + PyPI release**
- 🎨 improve docs theme & layout
- 🧪 add CI testing
- 📦 prepare **v0.2.0 roadmap**

Just say the word 🚀
```
