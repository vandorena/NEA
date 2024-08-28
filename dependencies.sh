#!~/
cd ~/


sudo apt update
sudo apt upgrade -y
git clone https://github.com/ecmwf/ecbuild.git
cd ecbuild
mkdir build
cd build
cmake ..
make
sudo make install
sudo apt iupdate && sudo apt upgrade -y
git clone https://gitlab.dkrz.de/k202009/libaec.git
cd libaec
mkdir build
cd build
cmake ..
make
sudo make install
sudo ldconfig
sudo apt update
sudo apt install gfortran -y
sudo apt update
sudo apt upgrade -y
sudo apt install -y build-essential cmake libssl-dev libcurl4-openssl-dev libpng-dev libopenjp2-7-dev libjpeg-dev zlib1g-dev
sudo apt install -y git
git clone https://github.com/ecmwf/eccodes.git
cd eccodes
mkdir build
cd build
cmake -DCMAKE_PREFIX_PATH=/usr/local -DCMAKE_Fortran_COMPILER=$(which gfortran) ..
make
sudo make install
echo 'export PATH="/usr/local/bin:$PATH"' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH="/usr/local/lib:$LD_LIBRARY_PATH"' >> ~/.bashrc
source ~/.bashrc
sudo apt install -y python3-pip
pip3 install eccodes
pip3 install numpy
pip3 install bokeh
pip3 install ecmwf.opendata
sudo apt update
sudo apt upgrade -y
