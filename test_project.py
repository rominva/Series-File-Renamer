from project import get_files, get_episode, generate_new_names, rename_system_files,remove_suffix, get_user_action, filter_files_with_episode
import pytest

def test_get_files_correct(tmp_path):
    # Temporary Path objects (using pytest mp_path fixture) 
    video = tmp_path / "FRIENDS S01E01-02.mkv"
    subtitle = tmp_path / "FRIENDS S01E01-02.srt"
    video_2 = tmp_path / "MODERN FAMILY S02E01.mp4"
    subtitle_2 = tmp_path / "MODERN FAMILY S02E01.vtt"
    sub = tmp_path / "sub.ass"
    clip = tmp_path / "clip_Hobbit.avi"
    clip_2 = tmp_path / "clip_HarryPotter.mov"
    photo = tmp_path / "photo.jpg"
    note = tmp_path / "notes.txt"
    song = tmp_path / "song.mp3"
    document = tmp_path / "word.docx"

    # Make temporary empty files (using Pathlib.Path.touch())
    video.touch()
    subtitle.touch()
    video_2.touch()
    subtitle_2.touch()
    sub.touch()
    clip.touch()
    clip_2.touch()  
    photo.touch()
    note.touch()
    song.touch()
    document.touch()

    result = get_files(str(tmp_path))
    expected = [video, subtitle, video_2, subtitle_2, sub, clip, clip_2]
    # assert sorted(result) == sorted(expected) 
    assert set(result) == set(expected)


def test_get_files_nonexistent_path(tmp_path):
    # 1) path exist but is not a directory
    file = tmp_path / "hello.py"
    file.touch()
    assert get_files(str(file)) is None

    # 2) path does not exist
    assert get_files("hello") is None


def test_get_files_empty_directory(tmp_path):
    assert get_files(str(tmp_path)) == []



def test_get_episode_supported():
    assert get_episode("The Untamed E01.mp4") == ("01", 13, 15)
    assert get_episode("The Untamed E01")[0] == "01"
    assert get_episode("Love Like The Galaxy [WEB-DL-480p] E52-end.avi")[0] == "52"
    assert get_episode("Birthcare Center [540p] E03 .mkv")[0] == "03"
    assert get_episode("2.Broke.Girls.S01E004.720p.Farsi.Sub.Film2Media.mov")[0] == "004"
    assert get_episode("Modern.FamilyS01.E6000.720P.Hard-Sub.Farsi.(Disfilm).mkv")[0] == "6000"
    assert get_episode("One.Piece.2023.S01E07 720p.10bit.WEBRip.2CH.x265.HEVC.PSA.Farsi.Sub.Film2Media.mkv")[0] == "07"
    assert get_episode("Sherlock.S01E800end.(A Study in Pink).720p.BluRay.x264.Dubbed.FA.vtt")[0] == "800"
    assert get_episode("Mr Sunshine20 [540p] E09.ass")[0] == "09"
    assert get_episode("FRIENDS [480p] S01E16-17.srt")[0] == "16-17"
    assert get_episode("2.Broke.Girls.S01E23E24.720p.Farsi.Sub.Film2Media-END")[0] == "23-24"
    assert get_episode(" E23E24") == ("23-24", 2, 7)


def test_get_episode_unsupported():
    assert get_episode("3-gatsu no Lion [480] 01.ass") is None
    assert get_episode("Arslan Senki [480p BD] 01.mkv") is None
    assert get_episode("Fugou Keiji - Balance - UNLIMITED [480p] 01.ass") is None
    assert get_episode("Show.01.720p.mkv") is None
    assert get_episode("Movie.480p.01.mkv") is None
    assert get_episode("Chocolate 1997-01-320p.mkv") is None
    assert get_episode("One Piece 2023 01 1080p.mkv") is None
    assert get_episode("One.Piece.2013.01.1080p.mkv") is None


def test_get_episode_not_fully_supported():
    assert get_episode(" E23 & E24")[0] != "23-24"
    assert get_episode(" E23-E24")[0] != "23-24"
    assert get_episode("Modern.FamilyS11.E23.24.720P.mkv")[0] != "23-24"
    assert get_episode("E23E24")[0] != "23-24"


def test_get_episode_invalid_input():
    assert get_episode("") is None



def test_generate_new_names(tmp_path):
    movie = tmp_path / "FRIENDS_480p_S01E01.mkv"
    sub = tmp_path / "FRIENDS_480p_S01E01.srt"
    movie_2 = tmp_path / "FRIENDS_480p_S01E02.mkv"
    sub_2 = tmp_path / "FRIENDS_480p_S01E02.srt"

    file_path_list = [movie, sub, movie_2, sub_2]


    desired_form_no_suffix = "FRIENDS [480p] 01"
    assert generate_new_names(file_path_list, desired_form_no_suffix) is None


    desired_form_no_suffix_2 = "FRIENDS [480p] S01E01"
    new_movie = tmp_path / "FRIENDS [480p] S01E01.mkv"
    new_sub = tmp_path / "FRIENDS [480p] S01E01.srt"
    new_movie_2 = tmp_path / "FRIENDS [480p] S01E02.mkv"
    new_sub_2 = tmp_path / "FRIENDS [480p] S01E02.srt"

    new_file_path_list = [new_movie, new_sub, new_movie_2, new_sub_2]
    assert generate_new_names(file_path_list, desired_form_no_suffix_2) == new_file_path_list


def test_generate_new_names_skips_files_without_episode(tmp_path):
    movie = tmp_path / "FRIENDS S01E01.mkv"
    invalid = tmp_path / "cover.jpg"
    movie_2 = tmp_path / "FRIENDS S01E02.mkv"

    file_path_list = [movie, invalid, movie_2]

    desired = "FRIENDS S01E01"

    expected = [
        tmp_path / "FRIENDS S01E01.mkv",
        tmp_path / "FRIENDS S01E02.mkv",
    ]

    assert generate_new_names(file_path_list, desired) == expected



def test_rename_system_files(tmp_path):
    old_path = tmp_path / "old.mkv"
    new_path = tmp_path / "new.mkv"

    old_path.touch()

    assert rename_system_files(old_path, new_path) == new_path
    assert new_path.exists()
    assert not old_path.exists()


def test_rename_system_files_existing_destination(tmp_path):
    old_path = tmp_path / "old.mkv"
    new_path = tmp_path / "new.mkv"

    old_path.touch()
    new_path.touch()

    with pytest.raises(FileExistsError):
        rename_system_files(old_path, new_path)



def test_remove_suffix():
    assert remove_suffix("FRIENDS S01E01-02.mkv") == "FRIENDS S01E01-02"
    assert remove_suffix("FRIENDS S01E01-02.srt") == "FRIENDS S01E01-02"
    assert remove_suffix("MODERN FAMILY S02E01.mp4") == "MODERN FAMILY S02E01"
    assert remove_suffix("MODERN FAMILY S02E01.vtt") == "MODERN FAMILY S02E01"
    assert remove_suffix("sub.ass") == "sub"
    assert remove_suffix("clip_Hobbit.avi") == "clip_Hobbit"
    assert remove_suffix("clip_HarryPotter.mov") == "clip_HarryPotter"

    assert remove_suffix("FRIENDS S01E01-02.MKV") == "FRIENDS S01E01-02"
    assert remove_suffix("FRIENDS S01E01-02.mKv") == "FRIENDS S01E01-02"


def test_remove_suffix_nosuffix():
    assert remove_suffix("The Untamed E01") == "The Untamed E01"


def test_remove_suffix_unacceptable():
    assert remove_suffix("photo.jpg") == "photo.jpg"


def test_remove_suffix_none():
    assert remove_suffix("") == ""



def test_get_user_action_correct_input(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda _: "a")
    assert get_user_action() == "a"

    monkeypatch.setattr("builtins.input", lambda _: "e")
    assert get_user_action() == "e"

    monkeypatch.setattr("builtins.input", lambda _: "q")
    assert get_user_action() == "q"

    monkeypatch.setattr("builtins.input", lambda _: " a ")
    assert get_user_action() == "a"

    monkeypatch.setattr("builtins.input", lambda _: "A")
    assert get_user_action() == "a"


def test_get_user_action_uncorrect_input(monkeypatch):
    user_inputs = iter(["x", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs))
    assert get_user_action() == "a"

    user_inputs_2 = iter(["aeq", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs_2))
    assert get_user_action() == "a"

    user_inputs_3 = iter(["ax", "a"])
    monkeypatch.setattr("builtins.input", lambda _: next(user_inputs_3))
    assert get_user_action() == "a"



def test_filter_files_with_episode(tmp_path):
    video = tmp_path / "FRIENDS S01E01-02.mp4"
    subtitle = tmp_path / "FRIENDS S01E01-02.srt"
    clip = tmp_path / "clip_Hobbit.mp4"
    sub = tmp_path / "sub.srt"

    file_path_list = [video, subtitle, clip, sub]

    file_path_list_with_ep = [video, subtitle]
    file_names_with_ep = ["FRIENDS S01E01-02.mp4", "FRIENDS S01E01-02.srt"]

    assert filter_files_with_episode(file_path_list) == (file_path_list_with_ep, file_names_with_ep)


def test_filter_files_with_episode_none(tmp_path):
    clip = tmp_path / "clip_Hobbit.mp4"
    sub = tmp_path / "sub.srt"

    file_path_list = [clip, sub]

    file_path_list_with_ep = []
    file_names_with_ep = []

    assert filter_files_with_episode(file_path_list) == (file_path_list_with_ep, file_names_with_ep)