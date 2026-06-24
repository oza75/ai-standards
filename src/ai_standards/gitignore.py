from pathlib import Path

_BEGIN = "# BEGIN ai-standards"
_END = "# END ai-standards"


class GitignoreManager:
    @staticmethod
    def add_paths(gitignore: Path, paths: list[str]) -> None:
        existing = gitignore.read_text(encoding="utf-8") if gitignore.exists() else ""

        block = _BEGIN + "\n" + "\n".join(paths) + "\n" + _END + "\n"

        if _BEGIN in existing:
            begin_pos = existing.index(_BEGIN)
            end_pos = existing.index(_END, begin_pos)
            # Advance past the _END line's trailing newline to preserve what follows
            end_line_end = end_pos + len(_END)
            if end_line_end < len(existing) and existing[end_line_end] == "\n":
                end_line_end += 1
            new_text = existing[:begin_pos] + block + existing[end_line_end:]
        else:
            separator = "\n" if existing and not existing.endswith("\n") else ""
            new_text = existing + separator + block

        gitignore.write_text(new_text, encoding="utf-8")

    @staticmethod
    def remove_block(gitignore: Path) -> None:
        if not gitignore.exists():
            return
        text = gitignore.read_text(encoding="utf-8")
        if _BEGIN not in text:
            return

        begin_pos = text.index(_BEGIN)
        end_pos = text.index(_END, begin_pos)
        end_line_end = end_pos + len(_END)
        if end_line_end < len(text) and text[end_line_end] == "\n":
            end_line_end += 1

        before = text[:begin_pos]
        after = text[end_line_end:]
        new_text = before + after
        # Collapse a double-blank introduced by removing the block
        if before.endswith("\n\n") and after.startswith("\n"):
            new_text = before.rstrip("\n") + "\n" + after

        gitignore.write_text(new_text, encoding="utf-8")
