# Checksum
## Installation
```
sudo apt install python3
sudo apt install python3-pip
pip3 install checksum-Pmk456
```
## Using DEB Package
```
wget https://github.com/pmk456/checksum/releases/download/checksum_amd64/checksum_amd64.deb
sudo dpkg -i checksum_amd64.deb
```
## Usage
```
usage: checksum [-h] [--hash HASH] [-a A] path

* Copyright of Patan Musthakheem, 2021 * Supports Checksum For SHA256, SHA1, MD5

positional arguments:
  path         Path of The File

optional arguments:
  -h, --help   show this help message and exit
  --hash HASH  Hash To Compare With
  -a A         Algorithm Of Hashing
```
