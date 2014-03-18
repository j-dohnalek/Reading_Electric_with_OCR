Description:
============

I have attempted to build a smart home using the Raspberry pi.
First part of my project is to read my electricity meter remaining credit. I have got a electricity meter which is topped up with key fob and has a display of one line of digits informing me about the remaining credit.
I have build a system using python 2.7 to take the picture of the display and I have used other software tools to convert the image to text.

There are many possible way for you to use it like taking picture of multimeters like some did to monitor home usage.

You will need:
==============

1) Gmail Account. I am using for this script gmail smtp service over the port 587. If you wish to send emails and you do not posses gmail account you will have to register for one.
Othervise you will have to find different service if you do not wish to use the gmail smtp.

2) SSOCR is a C library for optical character recognition which is desinged to read digits.You can install it from the commands bellow.

 * `sudo apt-get install libx11-dev`

 * `sudo apt-get install libimlib2-dev`

 * `wget http://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.14.1.tar.bz2`

 * `bzip2 -d ssocr-2.14.1.tar.bz2`

 * `tar xvf ssocr-2.14.1.tar`

 * `cd ssocr-2.14.1/`

 * `sudo make install`

3) imageMagic is library to convert images.

 * `sudo apt-get update`
 * `sudo apt-get install imagemagick`

4) crontabs

  To automatically generate crontab strings, I highly recommend using the following website:

 [http://www.corntab.com/pages/crontab-gui](http://www.corntab.com/pages/crontab-gui)
