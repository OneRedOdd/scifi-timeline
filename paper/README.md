# Paper

*Roads? Where We're Going: the movies promised me flying cars, so I kept score*, Andi Sharkey, October 2026.

- `paper.md`: source (Pandoc Markdown)
- `paper.docx`, `paper.pdf`: formatted versions
- `figures/`: figures used in the paper (regenerate with `python src/make_paper_figs.py`)

Read online: `docs/paper.html` on the project site.

See `findings/README.md` for where each file mentioned in the paper sits in this repository. Licence: CC BY 4.0.

`build_paper.py` rebuilds `paper.docx` and `paper.pdf` from `paper.md` (run it from inside `paper/`). It needs Pandoc, `pypandoc`, `python-docx` and LibreOffice, which are not in `requirements.txt`.
