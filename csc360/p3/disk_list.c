#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct disklist{
    char type_of_file;
    int file_size;
}disklist;

#define timeOffset 14 //offset of creation time in directory entry
#define dateOffset 16 //offset of creation date in directory entry

static unsigned int bytes_per_sector;

void print_date_time(char * directory_entry_startPos){
	
	int time, date;
	int hours, minutes, day, month, year;
	
	time = *(unsigned short *)(directory_entry_startPos + timeOffset);
	date = *(unsigned short *)(directory_entry_startPos + dateOffset);
	
	//the year is stored as a value since 1980
	//the year is stored in the high seven bits
	year = ((date & 0xFE00) >> 9) + 1980;
	//the month is stored in the middle four bits
	month = (date & 0x1E0) >> 5;
	//the day is stored in the low five bits
	day = (date & 0x1F);
	
	printf("%d-%02d-%02d ", year, month, day);
	//the hours are stored in the high five bits
	hours = (time & 0xF800) >> 11;
	//the minutes are stored in the middle 6 bits
	minutes = (time & 0x7E0) >> 5;
	
	printf("%02d:%02d\n", hours, minutes);
	
	return;	
}


void byt_per_sec(char *p){
	memcpy(&bytes_per_sector, (p + 11), 2);
	print_date_time(p + bytes_per_sector * 19);
}

char *concatenate(char *file_name, char *ext)
{
  int size = strlen(file_name) + strlen(".") + strlen(ext) + 1;
  char *str = malloc(size);
  strcpy (str, file_name);
  strcat (str, ".");
  strcat (str, ext); 

  return str;
}
char *get_file_name(char *file_name,char *p){
    
    char *ext = (char *)malloc(sizeof(char));
    for(int i =0; i < 8; i++){
        if(p[i] == ' '){
            i++;
            continue;}
        file_name[i] = p[i];
    }
    for(int j = 8 ; j < 12 ; j++){
        ext[j-8]=p[j];
    }
    file_name = concatenate(file_name,ext);
    free(ext);
    return file_name;
}
void print_disk_list(char *p){
    disklist *di = (disklist *)malloc(sizeof(disklist));
    char *file_name = (char *)malloc(sizeof(char));
    
    
    while(p[0]!=0x00 && *p<33*512){
        di->type_of_file = ((p[11]&0x10)==0x10) ? 'D':'F';
        file_name = get_file_name(file_name,p);
        if(p[11] == 0x0f || p[11] == 0x08 || di->type_of_file == 'D'){
            memset((void *)file_name,0,sizeof(file_name));
            //deal with sub-dir here.
            p+=32;
            continue;
        }
        int file_size = (p[28]&0xff)+((p[29]&0xff)<<8)+((p[30]&0xff)<<16)+((p[31]&0xff)<<24);
        printf("%c %10d %20s\n",di->type_of_file,file_size,file_name);
        //byt_per_sec(p);
        p+=32;
    }
    free(file_name);
}

int main(int argc, char *argv[]){
    int fd = open(argv[1],O_RDWR);
    if(argc != 2){
        fprintf(stderr,"Usage: ./disklist <file>\n");
        exit(1);
    }
    struct stat buffer;
    int status = fstat(fd,&buffer);
    if(status != 0){
        fprintf(stderr,"File image status error.\n");
        exit(1);
    }
    char *p = mmap(NULL, buffer.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); 
    if (p == MAP_FAILED) {
		printf("Error: failed to map memory\n");
		exit(1);
	}
    print_disk_list(p+512*19);
    munmap(p, buffer.st_size);
    close(fd);
    return 0;
}
