smart-home-raspcam
==================

Smart home automation with raspberry pi

Description:
============

I have attemp to build smart home using the Raspberry pi. First part of my project is to read my electricity meter. I have got a electricity meter which is topped up with key fob and have a display of one line of digits informing me about the remaing credit. I have build a system using python 2.7 to take the picture of the display and I have used other software tools to convert the image to text.

There are many possible way for you to use it like taking picture of multimeters like some did to monitor home usage.

You will need to install:
=========================

# 1) ssocr

sudo apt-get install libx11-dev

sudo apt-get install libimlib2-dev

wget http://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.14.1.tar.bz2

bzip2 -d ssocr-2.14.1.tar.bz2

tar xvf ssocr-2.14.1.tar

cd ssocr-2.14.1/

make

 
sudo make install

# 2) imageMagic 

sudo apt-get update
sudo apt-get install imagemagick

# 3) crontabs
