
.phony all:
all: sfs

sfs:
	gcc -Wall disk_info.c -o diskinfo
	gcc -Wall disk_list.c -o disklist
	gcc -Wall disk_get.c -o diskget
	

.PHONY clean:
clean:
	-rm -rf *.o *.exe
