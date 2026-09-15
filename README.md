# 📁 Series File Renamer v1

#### 🎥 Demo: <URL https://github.com/rominva/Series-File-Renamer/blob/main/assets/Series%20File%20Renamer%20v1%20-%20GIF%20Demo.gif>

#### 📝 Description:

**Series File Renamer v1** is a command-line Python program that helps users rename multiple video and subtitle files from a TV series at once.

The program asks the user to provide the full path of a folder and searches that folder for supported video and subtitle files. The supported file extensions are:

* 🎬 `.mp4`
* 🎬 `.mkv`
* 🎬 `.avi`
* 🎬 `.mov`
* 💬 `.srt`
* 💬 `.ass`
* 💬 `.vtt`

The program then tries to automatically determine the episode number from each filename. For an episode number to be recognized, the filename must contain one of the following episode indicators, case-insensitively:

* `e`
* `episode`

For example, filenames such as `Friends S01E05.mkv`, `Episode 12.mp4`, and `My.Series.episode13.srt` can be recognized because they explicitly identify the episode using `E`, `e`, `Episode`, or `episode`.

The program also supports filenames containing a range of episodes, such as `S02E16-17.mkv`, and attempts to preserve that episode range when generating the new filename.

### 🔄 How It Works

1. 📂 The user provides the full path of a folder.
2. 🔎 The program finds supported video and subtitle files.
3. 🔢 It identifies files containing an episode number.
4. ✏️ The user provides an example of the desired filename format.
5. 👀 The program generates and displays a preview of the new filenames.
6. ✅ The user can apply the changes, edit the naming format, or quit.
7. 🔄 If the user confirms, the program renames the files on the system.

Before making any changes, the program displays a preview showing the original and proposed new filenames. This gives the user an opportunity to check the results before the changes are applied permanently.

### ⚙️ Design Assumptions and Limitations

This is version 1 of the project, so it intentionally makes some simplifying assumptions.

📌 **Same-season assumption:**
I assume that all of the files in the selected folder belong to the **same season** of a series. Therefore, the program does not try to detect or modify the season number. The user can include the desired season number in the naming format they provide.

🔢 **Episode identification:**
The program requires the episode to be explicitly identified by `e` or `episode` (case-insensitive). This helps distinguish episode numbers from other numbers that may appear in filenames, such as release years, resolutions, or other metadata. For example, a number such as `2013` will not automatically be treated as an episode number merely because it appears in the filename.

⚠️ **Unsupported filenames:**
Files for which an episode number cannot be detected are not included in the renaming operation. The program informs the user which files could not be processed automatically.

⚠️ **Multiple episodes:**
Because this is version 1, multiple-episode filenames may not always be detected or handled perfectly. For this reason, the program displays a warning before the user permanently applies the changes and encourages the user to carefully review the preview.

### 🧪 Testing

The project includes a test file, `test_project.py`, written with `pytest`, which tests the main functions and different expected and invalid inputs.

### 📦 Dependencies

The main program uses only Python's standard library, including:

* `pathlib` for filesystem operations
* `re` for regular-expression matching

No external libraries are required to run the program.


### 👩‍💻Author:
Romina Valehi
