# Maintainer: Thanh Ha <thanh.ha@alumni.carleton.ca>
#
# Repository: https://github.com/Freeseer/freeseer

pkgname=freeseer-git
pkgver=20131006
pkgrel=1
pkgdesc="This project contains code for a video capture utility capable of capturing presentations. It captures vga output and audio and mixes them together to produce a video thus enabling you to capture great presentations, demos, or training material easily."
arch=('i686' 'x86_64')
url="https://github.com/Freeseer/freeseer"
license=('GPLv3')
groups=()
depends=(python2 python2-pyqt python2-feedparser gstreamer0.10-python python2-yapsy gstreamer0.10-good-plugins)
makedepends=(git)
optdepends=()
provides=()
conflicts=()
replaces=()
backup=()
options=()
install=
source=()
noextract=()
md5sums=() #generate with 'makepkg -g'

_gitroot="https://github.com/Freeseer/freeseer.git"

build() {
  git clone --depth 1 $_gitroot
  cd ${srcdir}/freeseer/
  git checkout -b pkgbuild origin/master
  cd src/

  cd freeseer/

  mkdir -p $pkgdir/usr/bin/
  mkdir -p $pkgdir/usr/lib/python2.7/site-packages/freeseer/
  sed "s/python/python2/g" ../freeseer-record > $pkgdir/usr/bin/freeseer-record
  sed "s/python/python2/g" ../freeseer-talkeditor > $pkgdir/usr/bin/freeseer-talkeditor
  sed "s/python/python2/g" ../freeseer-config > $pkgdir/usr/bin/freeseer-config
  chmod +x $pkgdir/usr/bin/freeseer-*
  cp *.py $pkgdir/usr/lib/python2.7/site-packages/freeseer/
  cp -r framework frontend plugins $pkgdir/usr/lib/python2.7/site-packages/freeseer/
}

