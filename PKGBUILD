# Maintainer: Angel Kilby <agkilby1@outlook.com>
pkgname=wepa-lpa-git
pkgver=2022.12.4
pkgrel=1
epoch=
pkgdesc="Wepa Print App"
arch=(x86_64)
url=""
license=('MIT')
groups=()
depends=(libgtk-3-0, libnotify4, libnss3, libxss1, libxtst6, xdg-utils, kde-cli-tools | kde-runtime | trash-cli | libglib2.0-bin | gvfs-bin, libcanberra-gtk-module, libcanberra-gtk3-module, cups)
makedepends=(git)
checkdepends=()
optdepends=()
provides=(wepa-lpa)
conflicts=(wepa-lpa)
replaces=()
backup=()
options=()
install=wepa-lpa.install
changelog=
source=("$pkgname-$pkgver.tar.gz"
        "$pkgname-$pkgver.patch")
noextract=()
sha256sums=()
validpgpkeys=()

prepare() {
	cd "$pkgname-$pkgver"
	patch -p1 -i "$srcdir/$pkgname-$pkgver.patch"
}

build() {
	cd "$pkgname-$pkgver"
	./configure --prefix=/usr
	make
}

package() {
	cd "$pkgname-$pkgver"
	make DESTDIR="$pkgdir/" install
}
