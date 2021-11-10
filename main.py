import shutil
import os
import glob
from pydub import AudioSegment
import youtube_dl
from spleeter.separator import Separator
from google.cloud import storage

# TODO: convert WAV to MP3

def yt_dl(video_url):
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    filename = f"/tmp/{video_info['title']}.mp3"
    options={
        'format':'bestaudio/best',
        'keepvideo':False,
        'outtmpl':filename,
    }

    with youtube_dl.YoutubeDL(options) as ydl:
        ydl.download([video_info['webpage_url']])

    print("Download complete... {}".format(filename))

    return filename

def spleeter(path_to_audio, path_to_directory):
    # Using embedded configuration.
    separator = Separator('spleeter:2stems')
    separator.separate_to_file(path_to_audio, path_to_directory)

def delete_folder(folder_path):
    shutil.rmtree(folder_path)

def delete_file(file_path):
    os.remove(file_path)

def upload_from_directory(directory_path: str, dest_bucket_name: str, dest_blob_name: str):
    gcs_client = storage.Client()
    rel_paths = glob.glob(directory_path + '/**', recursive=True)
    bucket = gcs_client.get_bucket(dest_bucket_name)
    for local_file in rel_paths:
        remote_path = f'{dest_blob_name}/{"/".join(local_file.split(os.sep)[1:])}'
        if os.path.isfile(local_file):
            blob = bucket.blob(remote_path)
            blob.upload_from_filename(local_file)

if __name__=='__main__':
    filename = yt_dl("https://www.youtube.com/watch?v=zHHcnjEJYQg")
    print(filename)
    spleeter(f"{filename}", "/tmp/")
    upload_from_directory(f"/tmp/{filename[5:-4]}", "splitted-songs", "test")
    delete_file(filename)
    delete_folder(f"/tmp/{filename[5:-4]}")