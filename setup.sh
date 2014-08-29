# create installation directory
cd /home/$USER/
mkdir install
cd install/

# install neccessary libraries for the ssocr
sudo apt-get install libx11-dev
sudo apt-get install libimlib2-dev

# download ssocr
wget http://www.unix-ag.uni-kl.de/~auerswal/ssocr/ssocr-2.14.1.tar.bz2
bzip2 -d ssocr-2.14.1.tar.bz2
tar xvf ssocr-2.14.1.tar
cd ssocr-2.14.1/

# install ssocr
sudo make install

# delete the installation directory
cd /home/$USER/
rm -rf install/

# install image magic
sudo apt-get update sudo apt-get install imagemagick
