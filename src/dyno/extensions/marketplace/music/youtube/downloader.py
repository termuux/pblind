from yt_dlp import YoutubeDL
import tempfile


def download_song(download_beacon ,download_directory):
    download_options={
    'format': 'm4a/webm',
    'outtmpl': download_directory.name+'/%(id)s',
    'quiet':'True'
    }
    print('Streaming {0} {1}'.format(download_beacon, '.'))
    
    try :
        youtube_dl = YoutubeDL(download_options)
        stream_metadata = youtube_dl.extract_info(f"ytsearch:{download_beacon}", download=True)['entries'][0]
    except Exception as exception_url:
        print('Cant stream {0}'.format(exception_url))
        raise

    return stream_metadata

def make_download_directory():
    download_directory = tempfile.TemporaryDirectory()
    return download_directory

def remove_download_directory(download_directory):
    try:
        download_directory.cleanup()
    except:
        pass