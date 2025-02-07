# Maintainer: Angel Kilby <agkilby1@outlook.com>
pkgname=wepa-lpa
pkgver=1
pkgrel=0
pkgdesc="Print App"
arch=(x86_64)
url=""
license=('MIT')
depends=()
makedepends=('git')
provides=()
conflicts=()
replaces=()
options=()
install=wepa-lpa.install
changelog=
source=("$pkgname-$pkgver.tar.gz"
        "$pkgname-$pkgver.patch")
noextract=()
sha256sums=(SKIP)
validpgpkeys=()

#prepare() {
#	cd "$pkgname-$pkgver"
#	patch -p1 -i "$srcdir/$pkgname-$pkgver.patch"
#}

build() {
	cd "$pkgname-$pkgver"
	./configure --prefix=/usr
	make
}

#check() {
#	cd "$pkgname-$pkgver"
#	make -k check
#}

package() {
	cd "$pkgname-$pkgver"
	make DESTDIR="$pkgdir/" install
}
