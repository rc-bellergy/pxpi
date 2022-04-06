# Voideo Stream using gstreamer
Tested OS: Debian Bullseye (Raspberry Pi)

## References
https://qengineering.eu/install-gstreamer-1.18-on-raspberry-pi-4.html

## Install a missing dependency

    sudo apt-get install libx264-dev libjpeg-dev

## Install the remaining plugins

    sudo apt-get update
    sudo apt-get install libgstreamer1.0-dev \
     libgstreamer-plugins-base1.0-dev \
     libgstreamer-plugins-bad1.0-dev \
     gstreamer1.0-plugins-ugly \
     gstreamer1.0-tools \
     gstreamer1.0-gl \
     gstreamer1.0-gtk3

## Install and build the missing plugins: e.g. 'h264parse'

    wget https://gstreamer.freedesktop.org/src/gst-plugins-bad/gst-plugins-bad-1.18.4.tar.xz
    sudo tar -xf gst-plugins-bad-1.18.4.tar.xz
    cd gst-plugins-bad-1.18.4
    mkdir build && cd build
    meson --prefix=/usr       \
       -D buildtype=release \
       -D package-origin=https://gstreamer.freedesktop.org/src/gstreamer/ \
       -D package-name="GStreamer 1.18.4 BLFS" ..
    ninja -j4
    sudo ninja install
    sudo ldconfig
