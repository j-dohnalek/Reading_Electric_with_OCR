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
        _camera_settings = {'co': 80,  # contrast
                            'iso': 800,  # ISO
                            'em': 'night',  # exposure mode
                            'mm': 'matrix',  # metering mode
                            'ss': 150000,  # shutter speed
                            'awb': 'auto'}  # white balance
    else:
        _camera_settings = camera_settings

    with picamera.PiCamera() as camera:
        camera.resolution = (resolution[0], resolution[1])
        camera.start_preview()
        camera.contrast = _camera_settings['co']
        camera.iso = _camera_settings['iso']
        camera.exposure_mode = _camera_settings['em']
        camera.meter_mode = _camera_settings['mm']
        camera.shutter_speed = _camera_settings['ss']
        camera.awb = _camera_settings['awb']
        # Give the camera some time to adjust to conditions
        sleep(2)
        camera.capture(imagename)
        camera.stop_preview()