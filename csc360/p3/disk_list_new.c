#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>

typedef struct disklist{
    char type_of_file;
    int time,date;
    int hours,minutes,day,month,year;
}disklist;

typedef struct dir_info{
    //char dir_name;
    int phys_num;// save number, minus 31+(p[26]+(p[27]<<8)) to get dirName. 32bytes each entry,224 entries in total.
}dir_info;

#define timeOffset 14 //offset of creation time in directory entry
#define dateOffset 16 //offset of creation date in directory entry


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


char *concatenate(char *file_name, char *ext){
  int size = strlen(file_name) + strlen(".") + strlen(ext) + 1;
  char *str = malloc(size);
  strcpy (str, file_name);
  strcat (str, ".");
  strcat (str, ext); 

  return str;
}

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
        return file_name; //directory name
    }
    
}

// char *get_file_name(char *file_name,char *p){    
//     char *ext = (char *)malloc(sizeof(char));
//     for(int i =0; i < 8; i++){
//         if(p[i] == ' '){
//             i++;
//             continue;}
//         file_name[i] = p[i];
//     }
//     for(int j = 8 ; j < 11 ; j++){
//         if(p[j] == ' '){
//             j++;
//             continue;}
//         ext[j-8]=p[j];
//     }
//     file_name = concatenate(file_name,ext);
//     free(ext);
//     return file_name;
// }

void get_file_from_subdir(char *dir_name, char *p){
    int physics = p[26]+(p[27]<<8)+31;
    printf("dir name: %s\n", dir_name);
    printf("logical:%d\n",(p[26]+(p[27]<<8)));
    printf("physics:%d\n",physics);
    
    //if((p[26]+(p[27]<<8)) == 0||1) no file in sub;

}

void print_disk_list(char *p){
    disklist *di = (disklist *)malloc(sizeof(disklist));
    char *file_name = (char *)malloc(sizeof(char));
    char *dir_name = (char *)malloc(sizeof(char));
    
    int count =0;
    while(p[0]!=0x00){
        di->type_of_file = ((p[11]&0x10)==0x10) ? 'D':'F';
            int logic_num = (p[26]+(p[27]<<8));
            if(di->type_of_file == 'D' && logic_num!=0x00 && logic_num!=0x01){
                //save dir infor. 
            }
            file_name = get_file_name(file_name,p,di->type_of_file);
            if(p[11] == 0x0f || p[11] == 0x08 ){
                memset((void *)file_name,0,sizeof(file_name));
                p+=32;
                continue;
            }   
        
            int file_size = (p[28]&0xff)+((p[29]&0xff)<<8)+((p[30]&0xff)<<16)+((p[31]&0xff)<<24);
            if(count == 0 ){
                printf("Root directory:\n");
                printf("==================\n");
                count++;
            }
            update_date_time(di,p);
            printf("%c %10d %20s ",di->type_of_file,file_size,file_name);
            printf("%d-%02d-%02d ", di->year, di->month, di->day);
            printf("%02d:%02d\n", di->hours, di->minutes);
            memset((void *)file_name,0,sizeof(file_name));//reset. 
            
        

        // else if(di->type_of_file == 'D'){
        //     dir_name = get_file_name(dir_name,p,di->type_of_file);
        //     if(p[11] == 0x0f || p[11] == 0x08 ){
        //         memset((void *)dir_name,0,sizeof(dir_name));
        //         p+=32;
        //         continue;
        //     }
        //     int file_size = (p[28]&0xff)+((p[29]&0xff)<<8)+((p[30]&0xff)<<16)+((p[31]&0xff)<<24);
        //     update_date_time(di,p);
        //     printf("%c %10d %20s ",di->type_of_file,file_size,file_name);
        //     printf("%d-%02d-%02d ", di->year, di->month, di->day);
        //     printf("%02d:%02d\n", di->hours, di->minutes);
        //     //find logical cluser num, corresponding physical cluser = num+31;
        //     //read every 32 bytes till 512 bytes 
        //     //get_file_from_subdir(dir_name,p);
        // }
        
        p+=32;
    }
    //after root finished,start print saved sub information.
    //printf("Sub directory:\n");
    //printf("==================\n");
    free(file_name);
    free(dir_name);
    free(di);
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
