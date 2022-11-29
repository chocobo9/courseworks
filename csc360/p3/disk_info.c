#include <sys/mman.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>


typedef struct diskinfo{
    char os_name[8];
    char lable[8];
    char byte_per_sec[2];
    char sec_count[2];
    char free_size[2];
    char num_files[1];
    char num_FAT[1];
}diskinfo;
void get_os_name(char *os_name, char *p){
    for (int i = 0;i<8;i++){
        os_name[i] = p[i+3];
    }
}
void get_label(char *label,char *p){
    p+= 512*19;
    while(p[0]!= 0x00){
        if(p[11] == 0x08){
            for(int j = 0; j<8; j++){
                label[j] = p[j];
            }
            
        }
        p+= 32;
    }
}
void get_free_size(int st_size,char *byte_per_sec,char *free_size, char *p){
    for(int i = 1; i<st_size/512; i++){
        
    }
    p+= 512;

}
int main(int argc, char *argv[]){
    int fd = open(argv[1], O_RDWR);
    if(argc != 2){
       fprintf(stderr,"Usage: ./diskinfo <file>\n");
       exit(1);
    }
    struct stat buffer;
    int status = fstat(fd,&buffer);
    if(status != 0){
        fprintf(stderr,"File image status error.\n");
        exit(1);
    }
    diskinfo *di = (diskinfo *)malloc(sizeof(diskinfo));
    char *p = mmap(NULL, buffer.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); 
    if (p == MAP_FAILED) {
		printf("Error: failed to map memory\n");
		exit(1);
	}
    
    *di->byte_per_sec = p[11]+(p[12]<<8);
    get_os_name(di->os_name,p);
    printf("OS Name: %s\n",di->os_name);
    get_label(di->lable,p);
    //printf("total:%d\n",(p[11]+(p[12]<<8))*(p[19]+(p[20]<<8)));
    
    printf("Label of the disk: %s\n",di->lable);
    get_free_size(buffer.st_size,di->byte_per_sec,di->free_size,p);
    printf("Total size of the disk: %ld\n",buffer.st_size);
    
    munmap(p, buffer.st_size); 
	close(fd);
    free(di);
    return 0;
}
