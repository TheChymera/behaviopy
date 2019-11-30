import math
import subprocess
from glob import glob
import os

import cv2
import numpy as np
from skimage.feature import canny
from skimage.filters import threshold_otsu
from skimage.measure import regionprops
from skimage.transform import pyramid_reduce, hough_circle, hough_circle_peaks
from skvideo.io import vread
from tqdm import tqdm

# OFT filenames
oft_filenames = [
  'nd750_a0072',
  'nd750_a0073',
  'nd750_a0074',
  'nd750_a0075',
  'nd750_a0076',
  'nd750_a0079',
  'nd750_a0080',
  'nd750_a0081',
  'nd750_a0082',
  'nd750_a0083',
  'nd750_a0084',
  'nd750_a0087',
  'nd750_a0088',
  'nd750_a0089',
  'nd750_a0090',
  'nd750_a0091',
  'nd750_a0092',
  'nd750_a0093',
  'nd750_a0098',
  'nd750_a0099',
  'nd750_a0100',
  'nd750_a0101',
  'nd750_a0102',
  'nd750_a0103',
  'nd750_a0104',
  'nd750_a0105',
  'nd750_a0106',
  'nd750_a0116',
  'nd750_a0117',
  'nd750_a0118',
  'nd750_a0119',
  'nd750_a0120',
  'nd750_a0121',
  'nd750_a0122',
  'nd750_a0123',
  'nd750_a0124',
  'nd750_a0134',
  'nd750_a0135',
  'nd750_a0136',
  'nd750_a0137',
  'nd750_a0138',
  'nd750_a0139',
  'nd750_a0140',
  'nd750_a0141',
  'nd750_a0142']


def load_results(path):
  """
  Load pickled results from videoprocessing session
  :param path: path to .npy file from one video
  :return: results dictionary
  """
  return np.load(path, allow_pickle=True).item()

class VideoProcessor():
  def __init__(self):
    pass

  def load_video(self,
                 path,
                 to_grey=True,
                 downscale=2):

    videodata = vread(path)
    imgs = []
    for img in tqdm(videodata):
      if to_grey:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      if downscale:
        img = pyramid_reduce(img, downscale=downscale)
      imgs.append(img)
    imgs = np.asarray(imgs)
    return imgs

  def calculate_median_image(self,
                             imgs,
                             percentage_beginning_end=0.1):
    ends = int(float(len(imgs)) * percentage_beginning_end)
    self.median_image = np.median(imgs[ends:int(len(imgs) - ends)],
                                  axis=0)

  def background_correct_videos(self,
                                imgs):
    self.calculate_median_image(imgs)
    imgs_corr = np.abs(imgs - self.median_image)
    return imgs_corr

  def extract_com_frame(self,
                        image):

    threshold = threshold_otsu(image, nbins=512)
    thresh = image > threshold
    labeled_foreground = (thresh).astype(int)
    properties = regionprops(labeled_foreground, thresh)
    center_of_mass = properties[0].centroid
    weighted_center_of_mass = properties[0].weighted_centroid

    return center_of_mass, \
           weighted_center_of_mass

  def extract_com_frames(self,
                         frames):

    print('extracting center of mass frame by frame')
    com_list = []
    fail_idx = 0
    for idx, img in tqdm(enumerate(frames)):
      try:
        center_of_mass, weighted_center_of_mass = self.extract_com_frame(img)
        com_list.append(center_of_mass)
      except IndexError:
        fail_idx = idx
        print('COM extraction failed for frame' + str(fail_idx) + ', skipping')

    return frames[fail_idx:], np.asarray(com_list)

  def get_videos(self,
                 path,
                 format='mp4',
                 behavior=None):

    videos = glob(path + '*.' + format)
    if behavior == 'OFT':
      res = []
      for video in videos:
        id = video.split('.')[0].split('/')[-1]
        if id in oft_filenames:
          res.append(video)
      return res
    return videos

  # TODO: parametrize
  def findRadius_circle(self,
                        images):

    try:
      self.median_image
    except AttributeError:
      self.calculate_median_image(images)
    edges = canny(self.median_image, sigma=0.2)
    hough_radii = np.arange(40, 80, 1)
    hough_res = hough_circle(edges, hough_radii)
    accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                               total_num_peaks=1)
    self.center_x, self.center_y, self.radius = cx[0], cy[0], radii[0]
    self.inner_circle_radius = int(self.radius * 0.75)

    return self.inner_circle_radius

  def label_frames(self,
                   com_list):

    labels = []
    for com in tqdm(com_list):
      norm = (com[1] - self.center_x) ** 2 + (com[0] - self.center_y) ** 2
      if norm < self.inner_circle_radius ** 2:
        labels.append(1)
      else:
        labels.append(0)

    return np.asarray(labels)

  def coordToPolar(self, x, y):
    r = np.sqrt(x ** 2 + y ** 2)
    phi = math.atan2(x, y)

    return r, phi

  def distance(self, x, y, x_prev, y_prev):
    return np.sqrt((x - x_prev) ** 2 + (y - y_prev) ** 2)

  def calculate_speed(self,
                      distances):
    x = range(0, len(distances))
    y = distances
    dx = np.diff(x)
    dy = np.diff(y)
    d = dy / dx

    return d

  def to_polar(self, com_list,
               normalize=True):

    x = com_list[:, 0]
    y = com_list[:, 1]
    # center coordinates
    x = x - self.center_x
    y = y - self.center_y
    # normalize by outer radius
    x = x / self.radius
    y = y / self.radius

    distances = [0.0]
    r = []
    phi = []
    for idx, el in enumerate(x):
      _r, _phi = self.coordToPolar(x[idx], y[idx])
      r.append(_r)
      phi.append(_phi)
      if idx == 0:
        continue
      else:
        new_dist = self.distance(x[idx], y[idx], x[idx - 1], y[idx - 1])
        distances.append(distances[-1] + new_dist)
    r = np.asarray(r)
    if normalize:
      r = r / self.radius
    return r, np.asarray(phi), np.asarray(distances)

  def mkv_to_avi(self, videos,
                 avi_path):
    for video in tqdm(videos):
      id = video.split('.')[0].split('/')[-1]

      command = 'ffmpeg -i ' + video + ' -vf scale=256:-1 -b 512k -flags global_header -vcodec mpeg1video -acodec copy ' + avi_path + id + '.avi'

      res = subprocess.run(command,
                           shell=True,
                           check=True, text=True)
    pass


def main():

  # adjust paths here
  basic_path_mkv = '/media/nexus/storage/christian_behavior_data/mkvs/'
  basic_path_avi = '/media/nexus/storage/christian_behavior_data/avi_oft_test/'
  results_path = '/media/nexus/storage/christian_behavior_data/results/'

  videoprocessor = VideoProcessor()

  # if only mkv available then do conversion
  videos = videoprocessor.get_videos(basic_path_mkv,
                                     format='mkv',
                                     behavior='OFT')

  if not os.path.exists(basic_path_avi):
    os.makedirs(basic_path_avi)
    # convert videos
    print('converting videos')
    videoprocessor.mkv_to_avi(videos, basic_path_avi)

  if not os.path.exists(results_path):
    os.makedirs(results_path)

  videos = videoprocessor.get_videos(basic_path_avi,
                                     format='avi')

  # now process all videos:
  for video in tqdm(videos):
    # adjust here for your specific filename
    filename = video.split('.avi')[0].split('_')[-1]
    print('filename')

    # load frames
    frames = videoprocessor.load_video(video)

    # create background substracted images
    corrected_imgs = videoprocessor.background_correct_videos(frames)

    # extract center of masses
    frames, com_list = videoprocessor.extract_com_frames(corrected_imgs)

    # detect radius for circular open field and calculate radius
    inner_circle_radius = videoprocessor.findRadius_circle(frames)

    # calculate for each frame if COM inside or outside that radius
    labels = videoprocessor.label_frames(com_list)

    # convert coordinates to polar coordinates
    r, phi, distances = videoprocessor.to_polar(com_list)

    # calculate speed
    speed = videoprocessor.calculate_speed(distances)

    # save results
    results = {
      'labels': labels,
      'com_list': com_list,
      'radii': r,
      'phi': phi,
      'distances': distances,
      'speed': speed,
      'inner_radius': inner_circle_radius,
      'example_frame' : frames[500],
    }

    np.save(results_path + filename + '_videoprocessing_results.npy', results)


if __name__ == "__main__":
  main()