from utils.utils import yt_dl, spleeter, convert_wav_to_mp3, upload_from_directory, delete_file, delete_folder
from fastapi import APIRouter

router = APIRouter()


@router.post("/url")
def split(url: str):
    filename = yt_dl(url)
    print(filename)
    spleeter(f"{filename}", "/tmp/")
    convert_wav_to_mp3(f"/tmp/{filename[5:-4]}")
    upload_from_directory(f"/tmp/{filename[5:-4]}", "splitted-songs", "songs")
    delete_file(filename)
    delete_folder(f"/tmp/{filename[5:-4]}")

@router.post("/local")
def split(path: str):
    filename = path
    spleeter(f"{filename}", "/tmp/")
    convert_wav_to_mp3(f"/tmp/{filename[5:-4]}")
    upload_from_directory(f"/tmp/{filename[5:-4]}", "splitted-songs", "songs")
    delete_file(filename)
    delete_folder(f"/tmp/{filename[5:-4]}")