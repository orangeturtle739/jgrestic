all: build/Makefile
	make --directory=build -j$(shell nproc) develop

format: build/Makefile
	make --directory=build -j$(shell nproc) format

build/Makefile:
	mkdir -p build
	cd build && cmake ..

.PHONY: clean
clean:
	test build/Makefile && make --directory=build clean
	rm -rf build
