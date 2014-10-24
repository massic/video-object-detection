'''
  Detection and classification use the 19-layer neural net from:
    Very Deep Convolutional Networks for Large-Scale Image Recognition
    K. Simonyan, A. Zisserman
    arXiv:1409.1556
  You can find information about this neural net here:
    https://gist.github.com/ksimonyan/3785162f95cd2d5fee77#file-readme-md
'''
from os.path import dirname, abspath, basename
from PIL import Image
import numpy as np
from datetime import datetime

from video_id_fetcher import get_nouns_and_video_ids
from video_fetcher import video_url, fetch_video
from image_utils import get_prepared_images
from classifier import classify
from detector import detect
from image_annotator import (draw_detector_results,
                             draw_classifier_results)
from image_utils import show_image


def where_is_noun_in_video(video_id, noun):
  '''
  Returns:
    a list of tuples of video segments in which that noun appears,
    in seconds. e.g. [(14.4, 20.2), (34.2, 89.2)]
  '''
  # TODO change 10,000 to 1,000 after the full pipeline works
  url = video_url(video_id)
  video_filename = fetch_video(url)
  image_dir = get_prepared_images(url, 10000, video_filename)
  predictions_filename = detect(image_dir, noun)
  draw_detector_results(predictions_filename, basename(image_dir), noun)

def show_nouns_in_videos(num_videos_per_noun):
  '''
  Run tail -f /tmp/detector_log.txt to see progress.
  '''
  log_filename = '/tmp/detector_log.txt'
  with open(log_filename, 'a') as f:
    for noun, video_id_list in get_nouns_and_video_ids(
                        num_videos_per_noun).iteritems():
      for i, video_id in enumerate(video_id_list):
        where_is_noun_in_video(video_id, noun)
        f.write(' '.join([str(datetime.now()),
                          noun,
                          video_id,
                          str(i) + '/' + str(num_videos_per_noun) + '\n',
                         ]))
        f.flush()

def test_classification(image_filename, noun):
  '''
  Classifies one BGR image and shows the results
  '''
  predictions = classify(image_filename)
  image = np.asarray(Image.open(
    draw_classifier_results(predictions, noun, image_filename)))
  Image.fromarray(image).save(
    'data/labelled-test-images/' + basename(image_filename))
  show_image(image)

def test_classification_of_bananas():
  image_that_contains_bananas = '/Users/rose/video-object-detection/' + \
                                'data/images/9uddKYGPEkg_10000/30000.jpg'

  # the same image above, but cropped to contain only bananas
  image_that_contains_only_bananas = '/Users/rose/' + \
    'video-object-detection/data/test-images/bananas_only_30000.jpg'

  images = [image_that_contains_bananas,
            image_that_contains_only_bananas]

  for image in images:
    test_classification(image, 'banana')

if __name__ == '__main__':
  show_nouns_in_videos(1)
