release:
	mkdir -p dist/
	tar -cf dist/docker-here.tar ./docker-here
	sha256sum docker-here > dist/CHECKSUMS

