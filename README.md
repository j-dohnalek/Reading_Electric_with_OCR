Description:
============

I have attemp to build smart home using the Raspberry pi. First part of my project is to read my electricity meter remaining credit. I have got a electricity meter which is topped up with key fob and have a display of one line of digits informing me about the remaing credit. I have build a system using python 2.7 to take the picture of the display and I have used other software tools to convert the image to text.

There are many possible way for you to use it like taking picture of multimeters like some did to monitor home usage.

You will need:
==============

1) https://pushover.net/ offers application 7500 messages montly for free, app to access it on android https://play.google.com/store/apps/details?id=net.superblock.pushover&ts=1413996231. For more information how to set up the Push over on Raspberry pi can be found on http://www.michaelhleonard.com/send-push-messages-from-beaglebone-black-or-raspberry-pi-to-iphone-or-android/ 

2) SSOCR is a C library for optical character recognition which is desinged to read digits.You can install it from the commands bellow.

sudo apt-get install libx11-dev

sudo apt-get install libimlib2-dev

wget http://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.14.1.tar.bz2

bzip2 -d ssocr-2.14.1.tar.bz2

tar xvf ssocr-2.14.1.tar

cd ssocr-2.14.1/

sudo make install

2) imageMagic is library to convert images. 

sudo apt-get update
sudo apt-get install imagemagick

3) crontabs

http://www.corntab.com/pages/crontab-gui
