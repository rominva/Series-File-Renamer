# Series File Renamer v1

from pathlib import Path
import re

VIDEO_EXTENSIONS = {".mp4", ".mkv", ".avi", ".mov"}
SUBTITLE_EXTENSIONS = {".srt", ".ass", ".vtt"}
SUPPORTED_SUFFIXES = VIDEO_EXTENSIONS | SUBTITLE_EXTENSIONS


def main():
    # Get the path from user
    folder = input("\n🔰 Please Enter Folder's Full Address:\n").strip()

    # Check the path for videos and subtitles
    file_path_list = get_files(folder)
    if file_path_list is None:
        # Stop the program if the path does not exist
        print("\n⭕ Path either does not exist or isn't a directory❗\n")
        return

    #  UX; Show the files to user
    print(f"\n🔶 Found {len(file_path_list)} supported_type file(s):\n")

    # Keep pathes with episode
    file_path_list_with_ep, file_names_with_ep = filter_files_with_episode(file_path_list)

    # Stop if there are no acceptable files at all
    if len(file_names_with_ep) == 0:
        print("\n⭕ Sorry this folder has no acceptable files❗\n")
        return

    # Show the first acceptable filename as an example
    print(f"\n🔆 Example:\n{file_names_with_ep[0]}\n")

    # Keep asking the user until we get acceptable answer
    while True:
        desired_form = input(
            "🔆 Enter the desired name for this file:\n> ").strip()  # str
        if not get_episode(desired_form):
            # Stop if form is acceptable
            print("\n⭕ Sorry, name is not acceptable. Try another name❗\n")
            continue

        # Remove the suffix so we can add it ourselves at the end
        desired_form_no_suffix = remove_suffix(desired_form)

        # List of file pathes with new names
        new_path_list = generate_new_names(file_path_list, desired_form_no_suffix)
        if not new_path_list:
            print(
                "\n⭕ Could not generate new filenames from the provided name.\nPlease try another name.")
            continue

        # Show the preview to the user
        print("\n\n🔷 Preview:\n")

        for old, new in zip(file_names_with_ep, new_path_list):
            print(f"{old}\n→ {new.name}\n")

        # Ask the user for confirmation before renaming
        user_check = get_user_action()

        if user_check == "q":
            print("\n\n🌌 Goodbye...\n")
            return
        elif user_check == "e":
            print()
            continue
        elif user_check == "a":
            print("\n⚠️ WARNING❗\nMultiple-episode files may not be detected correctly.\nPlease check the preview carefully before applying changes.")
            answer = input(
                "\n⛔ Apply these changes PERMANENTLY❓[y/n]: ").lower().strip()

            # Stop if the user changes their mind
            if answer != "y":
                print("\n\n🚫 OPERATION HAS STOPPED...\n")
                return

            # Change the filenames on the system
            for old_path, new_path in zip(file_path_list_with_ep, new_path_list):
                try:
                    rename_system_files(old_path, new_path)
                except FileExistsError:
                    print(f"This file already exists → {new_path}")
                    continue

            print("\n\n✅ Operation completed.\n")
            break


# Get supported files from the specified folder using pathlib
def get_files(folder_path: str) -> list[Path] | None:

    path = Path(folder_path)

    # Validate the path
    if not path.is_dir():
        return None

    file_path_list = []
    for item in path.iterdir():
        # Skip directories
        if item.is_file():
            if item.suffix in SUPPORTED_SUFFIXES:
                file_path_list.append(item)

    return file_path_list


# Find the episode and its location in a string
def get_episode(s: str) -> tuple[str, int, int] | None:
    pattern = r"[^a-zA-Z](e|episode)(?P<episode>\d+(-\d+)?)(e|episode)?(?P<episode_2>\d+(-\d+)?)?(\D|$)"
    if match := re.search(pattern, s, re.IGNORECASE):
        if match.group("episode_2"):
            episode = f"{match.group("episode")}-{match.group("episode_2")}"
            e_location = match.end("episode_2")
        else:
            episode = match.group("episode")
            e_location = match.end("episode")

        s_location = match.start("episode")
    else:
        return None

    return episode, s_location, e_location


# Generate new filenames for the preview
def generate_new_names(file_path_list: list[Path], desired_form_no_suffix: str) -> list[Path] | None:
    desired_form_ep = get_episode(desired_form_no_suffix)

    if not desired_form_ep:
        return None

    _, s_idx, e_idx = desired_form_ep

    new_path_list = []
    for path in file_path_list:
        # Check whether the episode exists
        result = get_episode(path.name)
        if result is None:
            continue

        path_ep = result[0]
        new_filename = desired_form_no_suffix[:s_idx] + path_ep + desired_form_no_suffix[e_idx:] + path.suffix
        new_path = path.parent / new_filename
        new_path_list.append(new_path)

    return new_path_list


# Rename files on the system
def rename_system_files(old_path: Path, new_path: Path) -> Path:

    return old_path.rename(new_path)


# Remove supported file suffix
def remove_suffix(desired_form: str) -> str:
    for suf in SUPPORTED_SUFFIXES:
        if desired_form.lower().endswith(suf):
            idx = len(suf)
            desired_form_no_suffix = desired_form[0 : -idx]
            break
    else:
        desired_form_no_suffix = desired_form

    return desired_form_no_suffix


def get_user_action() -> str:
    while True:
        user_check = input(
            "\n💠 What do you want to do?\n\n[a] Apply changes\n[e] Edit name\n[q] Quit\n--> ").lower().strip()
        if user_check in ["a", "e", "q"]:
            break
        print("\n⭕ Invalid choice. Please choose a, e, or q.")

    return user_check


def filter_files_with_episode(file_path_list: list[Path]) -> tuple[list[Path], list[str]]:
    file_path_list_with_ep = []
    file_names_with_ep = []

    for i, item in enumerate(file_path_list):
        name = item.name

        if get_episode(name):
            file_path_list_with_ep.append(item)
            file_names_with_ep.append(name)
            print(f"{i+1}. {name}")
        else:
            print(f"❌ Could not determine episode automatically for this file → {name}")

    return file_path_list_with_ep, file_names_with_ep


if __name__ == "__main__":
    main()
