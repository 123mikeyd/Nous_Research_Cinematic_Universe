# Rebuilding the browsing library

The source of truth is the existing Markdown archive plus `characters.json`. The site has no runtime dependencies: it serves static HTML, CSS, JavaScript and images.

From the repository root:

```sh
python -m pip install -r library/requirements.txt
python library/build.py
python -m http.server 8767 --bind 127.0.0.1
```

Open `http://127.0.0.1:8767/library/`.

## Editing

- Edit biographies and credits in `characters/*.md`, not in `library/read/`.
- Update names, evidenced aliases, profile paths and selected references in `library/characters.json`.
- `primary_reference` identifies the existing selected source art. `browse_preview` is its uncropped, lightweight derivative. Do not silently promote another sheet to primary.
- Add optimized previews to `images/previews/`, preserving originals separately. The current gallery previews fit within 640 × 640 pixels and preserve the full aspect ratio.
- Run the builder after changing content. It regenerates the README's delimited character-gallery region, alphabetical Markdown directory, HTML gallery, and reading pages. Handwritten README sections outside the gallery are preserved.
- All characters use the unified `nous` browsing group. Aliases are search terms, not separate roster entries.
- `publication_hold: true` removes the entry from generated front doors and removes previously generated readers for that profile and its sheets. It does not delete original archival files or rewrite Git history; review those separately before any publication.
- Teknium's alternate sheets require individual approval. For entries with `alternate_art_approval: individual-Mike-review-required`, the builder generates both the supplementary-art Markdown and reader from sheets explicitly marked `approval_status: approved-supplementary`. Only the anime alternate and chess-themed pose and expression sheet are approved; all other Teknium variants remain pending and are omitted. Each approved sheet has a `label`, a browsing `preview`, and an optional preserved `original` link. This does not change the primary reference. ee.dd uses the selected landscape avatar, not generated sheets.
- Run `python library/test_sheet_approval.py` to test individual approval and revocation in an isolated fixture.
- Model links remain optional, below prose and art. Cards must always open reading pages, never ZIP files.

Generated HTML can be served under a repository subdirectory, including GitHub Pages. Relative internal links do not depend on the domain. The source Markdown remains available alongside the static reader.

Rebuilding does not publish, commit, upload, or change repository settings.
