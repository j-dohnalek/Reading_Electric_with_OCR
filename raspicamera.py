__author__ = 'ihavelock'

import picamera
import sleep

# Resolution of the image from the camera
# better to keep is lower this will decrease
# the processing time


def take_picture(imagename, resolution=None, camera_settings=None):
    if resolution is None:
        resolution = [800, 600]

    if camera_settings is None:
        # camera settings
        camera_settings = {'co': 80,  # contrast
                           'iso': 800,  # ISO
                           'em': 'night',  # exposure mode
                           'mm': 'matrix',  # metering mode
                           'ss': 150000,  # shutter speed
                           'awb': 'auto'}  # white balance

    with picamera.PiCamera() as camera:
        camera.resolution = (resolution[0], resolution[1])
        camera.start_preview()
        camera.contrast = camera_settings['co']
        camera.iso = camera_settings['iso']
        camera.exposure_mode = camera_settings['em']
        camera.meter_mode = camera_settings['mm']
        camera.shutter_speed = camera_settings['ss']
        camera.awb = camera_settings['awb']
        # Give the camera some time to adjust to conditions
        sleep(2)
        camera.capture(imagename)
        camera.stop_preview()