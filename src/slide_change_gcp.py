from google.cloud import videointelligence
import os
import pickle
import youtube_dl
from google.cloud import storage


def my_hook(d):
    if d['status'] == 'finished':
        print('Done downloading, now uploading to gcloud ...')


def download_vid(url):
    # delete old video/subtitles
    if os.path.exists("videos/video123.en-US.vtt"):
        os.remove("videos/video123.en-US.vtt")
    if os.path.exists("videos/video123.mp4"):
        os.remove("videos/video123.mp4")

    # upload new video
    ydl_opts = {
        'format': '18',
        'outtmpl': 'videos/video123.mp4',
        'noplaylist': True,
        'writesubtitles': True,
        'allsubtitles': True,
        'progress_hooks': [my_hook],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def upload_blob(source_file_name, destination_blob_name):
    """Uploads a file to the bucket."""
    bucket_name = "hackathon_sahitya"
    # source_file_name = "local/path/to/file"
    # destination_blob_name = "storage-object-name"

    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    blob.upload_from_filename(source_file_name)

    print(
        "File {} uploaded to {}.".format(
            source_file_name, destination_blob_name
        )
    )


# set access to my google API key
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "gckey.json"


def process_vid(path_url):
    """ Detects camera shot changes. """
    video_client = videointelligence.VideoIntelligenceServiceClient()
    features = [videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
    operation = video_client.annotate_video(input_uri=path_url, features=features)
    print("\nProcessing video for shot change annotations:")

    result = operation.result(timeout=90)
    print("\nFinished processing.")

    shot_list = []

    # first result is retrieved because a single video was processed
    for i, shot in enumerate(result.annotation_results[0].shot_annotations):
        start_time = shot.start_time_offset.seconds + shot.start_time_offset.nanos / 1e9
        end_time = shot.end_time_offset.seconds + shot.end_time_offset.nanos / 1e9
        print("\tShot {}: {} to {}".format(i, start_time, end_time))
        shot_list.append((start_time, end_time))

    pickle.dump(shot_list, open("videos/slide_cuts.pkl", "wb"))
    print("All done!")

    return shot_list


def load_pkl():
    shot_list = pickle.load(open("videos/slide_cuts.pkl", "rb"))
    print(shot_list)


def video_to_transcript_cuts(video_url):
    download_vid(video_url)
    upload_blob("videos/video123.mp4", "video123.mp4")
    process_vid("gs://hackathon_sahitya/video123.mp4")
    # load_pkl()


if __name__ == "__main__":
    video_url = 'https://www.youtube.com/watch?v=XbIfFY_fJ_s'
    video_to_transcript_cuts(video_url)