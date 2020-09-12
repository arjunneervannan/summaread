from google.cloud import videointelligence
import io
import os


"""
THIS WORKS WELL!!
Extract timestamps, then summarize?
https://autosummarizer.com/
"""


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "../gckey.json"
path = "gs://hackathon_sahitya/covid_lecture_cut3.mp4"

# with io.open(path, "rb") as movie:
#     input_content = movie.read()

# operation = video_client.annotate_video(
#     features=features, input_content=input_content
# )

""" Detects camera shot changes. """
video_client = videointelligence.VideoIntelligenceServiceClient()
features = [videointelligence.enums.Feature.SHOT_CHANGE_DETECTION]
operation = video_client.annotate_video(input_uri=path, features=features)
print("\nProcessing video for shot change annotations:")

result = operation.result(timeout=90)
print("\nFinished processing.")

# first result is retrieved because a single video was processed
for i, shot in enumerate(result.annotation_results[0].shot_annotations):
    start_time = shot.start_time_offset.seconds + shot.start_time_offset.nanos / 1e9
    end_time = shot.end_time_offset.seconds + shot.end_time_offset.nanos / 1e9
    print("\tShot {}: {} to {}".format(i, start_time, end_time))