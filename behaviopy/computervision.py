import numpy as np
from tqdm import tqdm
from glob import glob
import math

import skvideo
import cv2
from skimage.transform import pyramid_reduce, hough_circle, hough_circle_peaks
from skimage.filters import threshold_otsu
from skimage.measure import regionprops
from skimage.feature import canny

class VideoProcessor():
  def __init__(self):
    pass

  def load_video(self,
                 path,
                 to_grey = True,
                 downscale=2):

    videodata = skvideo.io.vread(path)
    imgs = []
    for img in tqdm(videodata):
      if(to_grey):
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
      if(downscale):
        img = pyramid_reduce(img, downscale=downscale)
      imgs.append(img)
    imgs = np.asarray(imgs)
    return imgs


  def median_image(self,
                   imgs):
    return np.median(imgs[ends:int(len(imgs)-ends)]

  def background_correct_videos(self,
                            imgs,
                            percentage_beginning_end = 0.1):

    ends = int(float(len(imgs))*percentage_beginning_end)
    self.median_image = self.median_image(imgs)
    imgs_corr = np.abs(imgs - self.median_image,
                       axis=0))
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
        center_of_mass, weighted_center_of_mass = self.extractCOM(img)
        com_list.append(center_of_mass)
      except IndexError:
        fail_idx = idx
        print('COM extraction failed for frame' + str(fail_idx) + ', skipping')

    return frames[fail_idx:], np.asarray(com_list)

  def get_videos(self,
                 path,
                 format='mp4'):

    videos = glob(path + '*.' + format)
    return videos

  #TODO: parametrize
  def findRadius_circle(self,
                        images):

      if(not self.median_image):
        self.median_image = self.median_image(images)
      edges = canny(self.median_image, sigma=0.2)
      hough_radii = np.arange(40,80,1)
      hough_res = hough_circle(edges, hough_radii)
      accums, cx, cy, radii = hough_circle_peaks(hough_res, hough_radii,
                                                 total_num_peaks=1)
      self.center_x, self.center_y, self.radius = cx[0], cy[0], radii[0]
      self.inner_circle_radius = int(radius * 0.75)

      return self.inner_circle_radius

  def label_frames(self,
                   com_list):

    labels = []
    for com in tqdm(com_list):
        norm = (com[1]-self.center_x)**2 + (com[0]-self.center_y)**2
        if(norm < self.inner_circle_radius**2):
            labels.append(1)
        else:
            labels.append(0)

    return np.asarray(labels)

  def coordToPolar(x,y):
    r = np.sqrt(x**2 + y**2)
    phi = math.atan2(x,y)

    return r, phi

  def distance(x, y, x_prev, y_prev):
    return np.sqrt((x - x_prev) ** 2 + (y - y_prev) ** 2)

  def to_polar(self, com_list,
               normalize=True):

    x = com_list[:,0]
    y = com_list[:,1]
    # center coordinates
    x = x - self.center_x
    y = y - self.center_y
    # normalize by outer radius
    x = x/self.radius
    y = y/self.radius

    distances = []
    distances.append(0.0)
    r = []
    phi = []
    for idx, el in enumerate(x):
        _r, _phi = self.coordToPolar(x[idx], y[idx])
        r.append(_r)
        phi.append(_phi)
        if(idx==0):
            continue
        else:
            new_dist = self.distance(x[idx],y[idx], x[idx-1],y[idx-1])
            distances.append(distances[-1] + new_dist)
    r = np.asarray(r)
    if(normalize):
      r = r/self.radius
    return r, np.asarray(phi), np.asarray(distances)


def main():
  basic_path = '/media/nexus/storage/christian_behavior_data/mp4s/OFT/view_2_comp/'

  videoprocessor = VideoProcessor()
  videos = videoprocessor.get_videos(basic_path)

  # now process all videos:
  for video in videos:

    frames = videoprocessor.load_video(video)

    # skip frames (animal handling, etc)
    frames_to_skip = 100
    frames = frames[:frames_to_skip]

    # extract center of masses
    frames, com_list = videoprocessor.extract_com_frames(frames)

    # detect radius for circular open field and calculate radius
    inner_circle_radius = videoprocessor.findRadius_circle(frames)

    # calculate for each frame if COM inside or outside that radius
    labels = videoprocessor.label_frames(com_list)

    # convert coordinates to polar coordinates
    r, phi, distances = videoprocessor.to_polar(com_list)


if __name__ == "__main__":
  main()