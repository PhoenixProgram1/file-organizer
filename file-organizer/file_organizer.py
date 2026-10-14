import os
import shutil
import argparse
import logging
from pathlib import Path
from datetime import datetime

try:
    from colorama import Fore, Style, init
    init(autoreset=True)
    COLORAMA = True
except ImportError:
    COLORAMA = False

try:
    from tqdm import tqdm
    TQDM = True
except ImportError:
    TQDM = False


CATEGORIES = {
    "Images":     [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg",
                   ".webp", ".tiff", ".ico", ".heic"],
    "Videos":     [".mp4", ".mkv", ".mov", ".avi", ".wmv", ".flv",
                   ".webm", ".m4v", ".mpeg"],
    "Audio":      [".mp3", ".wav", ".flac", ".aac", ".ogg", ".m4a",
                   ".wma", ".opus"],
    "Documents":  [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt",
                   ".pptx", ".txt", ".csv", ".odt", ".rtf", ".md"],
    "Archives":   [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2",
                   ".xz", ".iso"],
    "Code":       [".py", ".js", ".ts", ".html", ".css", ".java",
                   ".cpp", ".c", ".cs", ".go", ".rb", ".php",
                   ".rs", ".sh", ".bat", ".json", ".xml", ".yaml",
                   ".yml", ".toml", ".ini", ".cfg"],
    "Executables":[".exe", ".msi", ".apk", ".dmg", ".deb", ".rpm"],
    "Fonts":      [".ttf", ".otf", ".woff", ".woff2"],
    "Misc":       [],
}


def _color(text: str, color: str) -> str:
    if not COLORAMA:
        return text
    colors = {
        "green":  Fore.GREEN,
        "yellow": Fore.YELLOW,
        "red":    Fore.RED,
        "cyan":   Fore.CYAN,
        "white":  Fore.WHITE,
    }
    return f"{colors.get(color, '')}{text}{Style.RESET_ALL}"


def setup_logging(log_file: str | None) -> logging.Logger:
    logger = logging.getLogger("file_organizer")
    logger.setLevel(logging.DEBUG)

    fmt = logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s",
                            datefmt="%Y-%m-%d %H:%M:%S")

    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    if log_file:
        fh = logging.FileHandler(log_file, encoding="utf-8")
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(fmt)
        logger.addHandler(fh)

    return logger


def get_category(extension: str) -> str:
    ext = extension.lower()
    for category, extensions in CATEGORIES.items():
        if ext in extensions:
            return category
    return "Misc"


def collect_files(directory: Path, recursive: bool) -> list[Path]:
    if recursive:
        return [p for p in directory.rglob("*") if p.is_file()]
    return [p for p in directory.iterdir() if p.is_file()]


def resolve_conflict(dest: Path) -> Path:
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    parent = dest.parent
    counter = 1
    while True:
        new_dest = parent / f"{stem}_{counter}{suffix}"
        if not new_dest.exists():
            return new_dest
        counter += 1


def organise(
    source_dir: str,
    output_dir: str | None,
    dry_run: bool,
    recursive: bool,
    log_file: str | None,
    undo_log: str | None,
) -> None:

    logger = setup_logging(log_file)
    src = Path(source_dir).resolve()

    if not src.exists():
        logger.error(_color(f"Source directory not found: {src}", "red"))
        return

    dest_root = Path(output_dir).resolve() if output_dir else src

    logger.info(_color(f"Source  : {src}", "cyan"))
    logger.info(_color(f"Output  : {dest_root}", "cyan"))
    logger.info(_color(f"Dry run : {dry_run}", "yellow"))

    files = collect_files(src, recursive)

    if not files:
        logger.info(_color("No files found. Nothing to do.", "yellow"))
        return

    logger.info(_color(f"Found {len(files)} file(s).", "white"))

    undo_entries: list[str] = []
    moved = skipped = errors = 0

    iterator = tqdm(files, unit="file") if TQDM else files

    for file_path in iterator:
        if file_path.resolve() == Path(__file__).resolve():
            continue

        category  = get_category(file_path.suffix)
        dest_dir  = dest_root / category
        dest_file = resolve_conflict(dest_dir / file_path.name)

        if dry_run:
            logger.info(f"  [DRY]  {file_path.name}  ->  {dest_file.relative_to(dest_root)}")
            skipped += 1
            continue

        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            shutil.move(str(file_path), str(dest_file))
            undo_entries.append(f"{dest_file}|{file_path}")
            logger.info(_color(f"  v  {file_path.name}  ->  {category}/", "green"))
            moved += 1
        except Exception as exc:
            logger.error(_color(f"  x  {file_path.name}  -  {exc}", "red"))
            errors += 1

    print()
    print(_color("-" * 50, "white"))
    print(_color(f"  Done!  Moved: {moved}  Skipped: {skipped}  Errors: {errors}", "cyan"))
    print(_color("-" * 50, "white"))

    if undo_log and undo_entries:
        with open(undo_log, "w", encoding="utf-8") as f:
            f.write("\n".join(undo_entries))
        logger.info(_color(f"Undo log saved: {undo_log}", "yellow"))


def undo(undo_log: str) -> None:
    logger = setup_logging(None)
    log_path = Path(undo_log)

    if not log_path.exists():
        logger.error(_color(f"Undo log not found: {undo_log}", "red"))
        return

    lines = log_path.read_text(encoding="utf-8").strip().splitlines()
    for line in lines:
        try:
            src, orig = line.split("|")
            shutil.move(src.strip(), orig.strip())
            logger.info(_color(f"  Restored: {Path(orig).name}", "green"))
        except Exception as exc:
            logger.error(_color(f"  x  {exc}", "red"))

    log_path.unlink()
    logger.info(_color("Undo complete. Log removed.", "yellow"))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="file_organizer",
        description="Sort files into categorized subfolders automatically.",
    )
    sub = p.add_subparsers(dest="command")

    org = sub.add_parser("run", help="Organise a directory.")
    org.add_argument("directory",
                     help="Directory to organise.")
    org.add_argument("-o", "--output",
                     help="Output root (default: same as source).",
                     default=None)
    org.add_argument("--dry-run", action="store_true",
                     help="Preview changes without moving anything.")
    org.add_argument("-r", "--recursive", action="store_true",
                     help="Recurse into subdirectories.")
    org.add_argument("--log",
                     help="Write detailed log to FILE.",
                     metavar="FILE", default=None)
    org.add_argument("--undo-log",
                     help="Save undo log to FILE.",
                     metavar="FILE",
                     default=f"undo_{datetime.now():%Y%m%d_%H%M%S}.log")

    u = sub.add_parser("undo", help="Reverse a previous run using its undo log.")
    u.add_argument("undo_log", help="Path to the undo log file.")

    return p


def main() -> None:
    parser = build_parser()
    args   = parser.parse_args()

    if args.command == "run":
        organise(
            source_dir=args.directory,
            output_dir=args.output,
            dry_run=args.dry_run,
            recursive=args.recursive,
            log_file=args.log,
            undo_log=args.undo_log,
        )
    elif args.command == "undo":
        undo(args.undo_log)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
