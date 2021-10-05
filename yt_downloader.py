import youtube_dl
from spleeter.separator import Separator


def yt_dl():
    video_url = input("please enter youtube video url:")
    video_info = youtube_dl.YoutubeDL().extract_info(
        url = video_url,download=False
    )
    filename = f"songs/{video_info['title']}.mp3"
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



if __name__=='__main__':
    #filename = yt_dl()
    spleeter('songs/Django - Juin.mp3', "songs/")