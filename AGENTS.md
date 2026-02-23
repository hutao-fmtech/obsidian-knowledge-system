# Repository Guidelines

## Project Structure & Module Organization
The vault follows PARA conventions: `02-项目/` holds active projects with deadlines, `03-领域/` tracks ongoing domains, `04-资源/` stores reference material, `10-卡片盒/` keeps atomic Zettelkasten notes, and `20-日志/` contains daily/weekly/monthly journals under dated subfolders (for example `20-日志/日记/2026/01/2026-01-26.md`). System documentation, templates, and dashboards live in `00-系统/`, while `90-附件/` safeguards supporting assets. Create or move notes according to the decision tree in `00-系统/📖 使用手册.md`. Never leave content at the vault root.

## Build, Test, and Development Commands
This is a documentation repository, so "build" equals validation. Favor `rg` for searching: `rg --files "02-项目" -g "*.md"` lists all project notes. Run `rg -L "^---" -g"*.md"` to catch missing frontmatter and `rg -L "^tags:" -g"*.md"` to surface untagged notes. Measure inbox debt with `find "01-收件箱" -name "*.md" | wc -l`.

## Coding Style & Naming Conventions
All content is Markdown with YAML frontmatter. Start every file with `---` blocks that include `title`, `created`, `updated`, and `tags` (Chinese tags only). Honor emoji headings from the templates (e.g., `## 💡 核心观点`). Follow naming rules: journals use ISO dates, weekly files `YYYY-Wxx`, monthly `YYYY-MM`, resources `《书名》- 作者.md`, and atomic insights concise nouns. Notes must include at least two wikilinks like `[[标签体系设计]]` to avoid orphans.

## Testing Guidelines
Manually verify changes after edits: rerun the frontmatter/tag checks above, review backlinks to confirm bidirectional links, and skim Dataview queries in affected notes so their field names remain untouched. When adding tasks or metadata, ensure emoji remain intact and update the `updated` timestamp. Store screenshots in `90-附件/` and reference them relative to the note.

## Commit & Pull Request Guidelines
Use imperative, scope-focused commit subjects (e.g., `Add project template guide`). Describe impacted directories in the body and mention validation commands executed. Ensure `git status` shows no stray files outside sanctioned folders, and avoid touching `.obsidian`. Pull requests should summarize the intent, list main files edited, link related issues or MOC entries, and call out any manual steps reviewers must repeat (such as running the frontmatter scan).

## Agent Workflow Tips
Start by checking `01-收件箱/` for items to process, consult the matching template inside `00-系统/templates/`, and only then create or edit notes. Move files promptly after creation, keep Chinese as the default language, and document upstream/downstream wikilinks so the graph stays bidirectional.
