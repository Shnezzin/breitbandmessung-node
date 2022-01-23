#!/bin/sh
arch=$(uname -m)
if [ $os = "Linux" ] ; then
    case "$arch" in
        i386 | i486 | i786 | x86)
            url=https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux32.tar.gz
            ;;        
        x86_64 | x86-64 | x64 | amd64)
            url=https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz
            ;;
        xscale | arm | armv61 | armv71 | armv81 | aarch64)
            url=https://github.com/shneezin/breitbandmessung/raw/dev/geckodriver-v0.30.0-linuxarm32.tar.gz
            ;;
        *)
            echo Architecture not supported: $arch
            exit 1
            ;;
    esac
elif [ $os = "Darwin" ] ; then
    url=https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-macos.tar.gz
fi

if [ -z $url ] ; then
    echo OS not supported: $os
    exit 1
fi

echo $url

curl -s -L "$url" | tar -xz
chmod +x geckodriver
mv geckodriver /usr/bin
