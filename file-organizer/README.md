# File Organizer

![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=flat-square&logo=python)
![License](https://img.shields.io/badge/license-MIT-green?style=flat-square)
![Version](https://img.shields.io/badge/version-1.0.0-orange?style=flat-square)

A lightweight CLI tool that automatically sorts files in any directory into clean, categorized subfolders with dry-run preview, recursive mode, full logging, and a one-command undo.

---

## Features

- Auto-categorizes files into: `Images`, `Videos`, `Audio`, `Documents`, `Archives`, `Code`, `Executables`, `Fonts`, `Misc`
- Dry-run mode to preview every move before anything actually happens
- Recursive mode to optionally dig into subdirectories
- Conflict resolution that never overwrites and renames duplicates automatically
- Undo support via auto-generated log files
- Colored output via `colorama`
- Progress bar via `tqdm`

---

## Requirements

- Python 3.10+
- `colorama`
- `tqdm`

---

## Installation

### Windows

Double-click `install.bat` to install all dependencies automatically.

### Manual

```bash
git clone https://github.com/your-username/file-organizer.git
cd file-organizer
pip install -r requirements.txt
```

---

## Usage

### Basic

```powershell
python file_organizer.py run "C:\Users\You\Downloads"
```

### Dry run

```powershell
python file_organizer.py run "C:\Users\You\Downloads" --dry-run
```

### Recursive

```powershell
python file_organizer.py run "C:\Users\You\Downloads" -r
```

### Output to a different folder

```powershell
python file_organizer.py run "C:\Users\You\Downloads" -o "D:\Sorted"
```

### Save a log file

```powershell
python file_organizer.py run "C:\Users\You\Downloads" --log run.log
```

### Undo the last run

```powershell
python file_organizer.py undo undo_20261014_155515.log
```

Every run generates an undo log automatically named `undo_YYYYMMDD_HHMMSS.log`. Pass it to the `undo` command to move everything back exactly where it was.

---

## Example Output

```
2026-10-14 15:55:15  INFO      Source  : C:\Users\admin\Downloads
2026-10-14 15:55:15  INFO      Found 22 file(s).
2026-10-14 15:55:15  INFO        v  photo.jpg       -> Images/
2026-10-14 15:55:15  INFO        v  resume.pdf      -> Documents/
2026-10-14 15:55:15  INFO        v  backup.zip      -> Archives/
2026-10-14 15:55:15  INFO        v  setup.exe       -> Executables/

--------------------------------------------------
  Done!  Moved: 22  Skipped: 0  Errors: 0
--------------------------------------------------
```

---

## Output Structure

```
Downloads/
├── Images/
│   ├── photo.jpg
│   └── screenshot.png
├── Videos/
│   └── clip.mp4
├── Documents/
│   ├── resume.pdf
│   └── notes.txt
├── Code/
│   └── script.py
├── Executables/
│   └── setup.exe
└── Archives/
    └── backup.zip
```

---

## Category Map

| Category    | Extensions                                            |
|-------------|-------------------------------------------------------|
| Images      | jpg, jpeg, png, gif, bmp, svg, webp, tiff, ico, heic  |
| Videos      | mp4, mkv, mov, avi, wmv, flv, webm, m4v, mpeg         |
| Audio       | mp3, wav, flac, aac, ogg, m4a, wma, opus              |
| Documents   | pdf, doc, docx, xls, xlsx, ppt, pptx, txt, csv, md   |
| Archives    | zip, rar, 7z, tar, gz, bz2, xz, iso                  |
| Code        | py, js, ts, html, css, java, cpp, c, cs, go, rb, ... |
| Executables | exe, msi, apk, dmg, deb, rpm                          |
| Fonts       | ttf, otf, woff, woff2                                 |
| Misc        | everything else                                       |

---

## License

MIT
