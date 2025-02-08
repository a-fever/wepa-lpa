# Maintainer: Angel Kilby <agkilby1@outlook.com>
pkgname=wepa-lpa
pkgver=1
pkgrel=0
pkgdesc="Wepa Print Application"
arch=(x86_64)
url="www.wepanow.com"
license=('MIT')
depends=()
makedepends=('git')
provides=()
conflicts=()
replaces=()
install=wepa-lpa.install
source=("$pkgname-$pkgver::git://github.com/a-fever/wepa-lpa.git")
#noextract=()
sha256sums=('SKIP')


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
