import shutil
import os
import glob
from pydub import AudioSegment
import youtube_dl
from spleeter.separator import Separator
from google.cloud import storage


def yt_dl(video_url: str):
    video_info = youtube_dl.YoutubeDL().extract_info(url=video_url, download=False)
    filename = f"/tmp/{video_info['title']}.mp3"
    options = {
        "format": "bestaudio/best",
        "keepvideo": False,
        "outtmpl": filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info["webpage_url"]])

    print("Download complete... {}".format(filename))

    return filename


def spleeter(path_to_audio: str, path_to_directory: str):
    # Using embedded configuration.
    separator = Separator("spleeter:2stems")
    separator.separate_to_file(path_to_audio, path_to_directory)


def convert_wav_to_mp3(folder_path):
    rel_paths = glob.glob(folder_path + "/**", recursive=True)
    for local_file in rel_paths:
        if local_file[-4:] == ".wav":
            AudioSegment.from_wav(local_file).export(
                f"{local_file[:-4]}.mp3", format="mp3"
            )
            delete_file(local_file)


def delete_folder(folder_path: str):
    shutil.rmtree(folder_path)


def delete_file(file_path: str):
    os.remove(file_path)


def upload_from_directory(
    directory_path: str, dest_bucket_name: str, dest_blob_name: str
):
    gcs_client = storage.Client()
    rel_paths = glob.glob(directory_path + "/**", recursive=True)
    bucket = gcs_client.get_bucket(dest_bucket_name)
    for local_file in rel_paths:
        print(local_file)
        tmp_path = "/".join(local_file.split(os.sep)[1:])
        remote_path = f"{dest_blob_name}/{tmp_path[4:]}"
        if os.path.isfile(local_file):
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)
