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
    char lable[12];
    int byte_per_sec;
    int sec_count;
    int free_size;
    int num_files;
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
            break;
        }
        p+= 32;
    }
}

int get_total_sector(char *p){
    return p[19]+(p[20]<<8);
}//copy
int get_sector_fat(char *p){
    return p[22]+(p[23]<<8);
}//copy

/**
 * @brief Get the FAT value.
 * 
 * @param n cluster number.
 * @param p image pointer
 * @return FAT value.
 */
int get_fat_val(int n, char *p){

    int low_bits, high_bits;

    if(n % 2 == 0){
        low_bits = p[512+(n*3)/2+1]&0x0f;
        high_bits = p[512+(n*3)/2]&0xff;
        return (low_bits<<8)+high_bits;
    }else{
        high_bits = p[512 + (n*3)/2]&0xf0;
        low_bits = p[512 + (n*3)/2+1]&0xff;
        return (high_bits>>4)+(low_bits<<4);
    } 
}

int get_free_size(char *p){
    int unused = 0;

    for(int i = 2; i<(p[19]+(p[20]<<8))-31; i++){
        if(get_fat_val(i,p) == 0x00){
            unused++;
        }
    }
    p+= 512;
    return unused * 512;
}//copy

int get_file_num(char *p){
    p+=512*19;
    int n = 0;
    for(int i = 0; i < 224 ; i++,p+=32){
        if(p[11]==0x0f || p[11] == 0x08){
            continue;
        }
        else if(((p[0]&0xff) == 0xE5) || ((p[0]&0xff) == 0x00)){
            continue;
        }
        else if((p[26]+(p[27]<<8))<2){
            continue;
        }
        n++;
    }
    return n;
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
    
    di->byte_per_sec = p[11]+(p[12]<<8);
    get_os_name(di->os_name,p);
    printf("OS Name: %s\n",di->os_name);
    
    get_label(di->lable,p);
    printf("Label of the disk: %s\n",di->lable);

    di->free_size = get_free_size(p);
    di->num_files = get_file_num(p);
    int sectorFat = get_sector_fat(p);
    printf("Total size of the disk: %ld bytes\n",buffer.st_size);
    printf("Free size of the disk:%d bytes\n\n",di->free_size);
    printf("==================\n");
    printf("The number of files in the image: %d \n\n",di->num_files);
    printf("==================\n");
    printf("Number of fat copies:%d\n",p[16]);
    printf("Sectors per Fat:%d\n", sectorFat);
    
    munmap(p, buffer.st_size); 
	close(fd);
    free(di);
    return 0;
}
