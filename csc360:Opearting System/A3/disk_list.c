#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
/**
 * @brief save data of image.
 * 
 */
typedef struct disklist{
    char type_of_file;
    int time,date;
    int hours,minutes,day,month,year;
    int dir_save[250];
    int count;
}disklist;


#define timeOffset 14 //offset of creation time in directory entry
#define dateOffset 16 //offset of creation date in directory entry

/**
 * @brief help code from tutorial
 * 
 * @param di Image pointer.
 * @param directory_entry_startPos start position.
 */
void update_date_time(disklist *di,char *directory_entry_startPos){
	
	di->time = *(unsigned short *)(directory_entry_startPos + timeOffset);
	di->date = *(unsigned short *)(directory_entry_startPos + dateOffset);
	
	//the year is stored as a value since 1980
	//the year is stored in the high seven bits
	di->year = ((di->date & 0xFE00) >> 9) + 1980;
 
	//the month is stored in the middle four bits
	di->month = (di->date & 0x1E0) >> 5;
   
	//the day is stored in the low five bits
	di->day = (di->date & 0x1F);

	//the hours are stored in the high five bits
	di->hours = (di->time & 0xF800) >> 11;
    
	//the minutes are stored in the middle 6 bits
	di->minutes = (di->time & 0x7E0) >> 5;
}
/**
 * @brief concatenate file name , '.' and the extension.
 * 
 * @param file_name 
 * @param ext the extension of the file.
 * @return full file name.
 */
char *concatenate(char *file_name, char *ext){
  int size = strlen(file_name) + strlen(".") + strlen(ext) + 1;
  char *str = malloc(size);
  strcpy (str, file_name);
  strcat (str, ".");
  strcat (str, ext); 

  return str;
}
/**
 * @brief Get the file name + '.' + the extension or the sub directory in the root directory.
 * 
 * @param file_name read file name from pointer.
 * @param p image pointer.
 * @param addr file name address.
 * @return full file name.
 */
char *get_file_name(char *file_name,char *p,char f_type){
    if(f_type == 'F'){
        char *ext = (char *)malloc(sizeof(char));
        for(int i =0; i < 8; i++){
            if(p[i] == ' '){
                i++;
                continue;}
            file_name[i] = p[i];
        }   
        for(int j = 8 ; j < 12 ; j++){
            if(p[j] == ' '){
                j++;
                continue;}
            ext[j-8]=p[j];
        }
        file_name = concatenate(file_name,ext);
        free(ext);
        return file_name;
    }
    else{
        for(int i =0; i < 8; i++){
            if(p[i] == ' '){
                i++;
                continue;}
            file_name[i] = p[i];
        }
        file_name[7] = '\0';
        return file_name; //directory name
    }
    
}
/**
 * @brief unfinished.
 * 
 * @param di 
 * @param p 
 * @param dir 
 */
void print_from_subdir(disklist *di, char *p,int dir){
    //int physics = p[26]+(p[27]<<8)+31;
    char *dir_name = (char *)malloc(sizeof(char));
    while(p[0]!=0x00){
        if(p[11] == 0x0f || p[11] == 0x08 ){
            memset((void *)dir_name,0,sizeof(dir_name));
            p+=32;
            continue;
        }  
        printf("\n%s\n",get_file_name(dir_name,p,di->type_of_file));
        printf("==================\n");
        p+=32;
    }
    free(dir_name); 
}
/**
 * @brief print file information as instruction.
 * 
 * @param di struct to save information. 
 * @param p Image pointer
 * @param dir start position.Was trying to keep updating this var to make function recurssive.
 */
void print_disk_list(disklist *di,char *p,int dir){
    
    char *file_name = (char *)malloc(sizeof(char));
    
    
    di->count = -1;
    int n = 0;
    while(p[0]!=0x00){
        di->type_of_file = ((p[11]&0x10)==0x10) ? 'D':'F';
        di->count++;
        if(di->type_of_file == 'D'){
            di->dir_save[n++] = di->count;
        }
        
        file_name = get_file_name(file_name,p,di->type_of_file);
        
        if(p[11] == 0x0f || p[11] == 0x08 ){
            memset((void *)file_name,0,sizeof(file_name));
            p+=32;
            continue;
        }   
        int file_size = (p[28]&0xff)+((p[29]&0xff)<<8)+((p[30]&0xff)<<16)+((p[31]&0xff)<<24);
        update_date_time(di,p);
        printf("%c %10d %20s ",di->type_of_file,file_size,file_name);
        printf("%d-%02d-%02d ", di->year, di->month, di->day);
        printf("%02d:%02d\n", di->hours, di->minutes);
        memset((void *)file_name,0,sizeof(file_name));//reset. 
        p+=32;
    }
    free(file_name);
    
}

int main(int argc, char *argv[]){
    int fd = open(argv[1],O_RDWR);
    int dir = 0;
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
    disklist *di = (disklist *)malloc(sizeof(disklist));
    printf("Root directory:\n");
    printf("==================\n");
   
    print_disk_list(di,p+512*19,dir);
    munmap(p, buffer.st_size);
    close(fd);
    return 0;
}
