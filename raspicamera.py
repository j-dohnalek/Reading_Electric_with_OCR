__author__ = 'ihavelock'

import picamera
import sleep

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

    # a type assertion here would be good as you validate that format of the list that is submitted for resolution.
    # lines that begin with ### are lines of code.

    # So first we assert that resolution is in fact a list object.
    ### assert isinstance(resolution, list):
        # if it is a list, we need to know it's length, i.e. how many items are in the list as we only want 2 items!
        ### if len(resolution) = 2:
            # we now need to know if each entry in the list is a number
            ### for entry in resolution:
                ### assert isinstance(entry, int):
                    # Now that we are sure that the resolution submitted is correct, we can assign it.
                    ### _resolution = resolution
        ### else:
                ### resolution = [800, 600]
                ### print "Something went wrong."

    if resolution is None:
        resolution = [800, 600]

    # there is a more resilient way of specifying this to make this more re-usable.
    if camera_settings is None:
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