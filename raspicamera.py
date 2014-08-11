import subprocess
import picamera
import time

# Resolution of the image from the camera
# better to keep is lower this will decrease
# the processing time


def take_picture(imagename, resolution=None, camera_settings=None):
    """

    :param imagename:  name of the image that you want to create
    :param resolution:  image resolution to save as.  Default is 800x600
    :param camera_settings:  the settings for the camera.  Defaults are:
        camera_settings dict:   {
                                'co': 80,        # contrast
                                'iso': 800,      # ISO
                                'em': 'night',   # exposure mode
                                'mm': 'matrix',  # metering mode
                                'ss': 150000,    # shutter speed
                                'awb': 'auto'    # white balance
                                }
    """

    if resolution is None:
        resolution = [800, 600]

    # there is a more resilient way of specifying this to make this more re-usable.
    if camera_settings is None:
        _camera_settings = {'co': 25,  # contrast
                            'iso': 640,  # ISO
                            'em': 'night',  # exposure mode
                            'mm': 'spot',  # metering mode
                            'sh': 80, 
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
        camera.sharpness = 100
        camera.awb = _camera_settings['awb']
        # Give the camera some time to adjust to conditions
        time.sleep(2)
        camera.capture(imagename)
        camera.stop_preview()
