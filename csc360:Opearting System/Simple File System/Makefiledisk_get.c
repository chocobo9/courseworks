#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <sys/mman.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <unistd.h>
#include <ctype.h>
#include <string.h>


#define LAST_CLUSTER 0xfff

/**
 * @brief concatenate file name , '.' and the extension.
 * 
 * @param file_name 
 * @param ext the extension of the file.
 * @return full file name.
 */
char *concatenate(char *file_name, char *ext)
{
  int size = strlen(file_name) + strlen(".") + strlen(ext) + 1;
  char *str = malloc(size);
  strcpy (str, file_name);
  strcat (str, ".");
  strcat (str, ext); 

  return str;
}

/**
 * @brief Get the file name + '.' + the extension. Same with my disk_list.c.
 * 
 * @param file_name read file name from pointer.
 * @param p image pointer.
 * @param addr file name address.
 * @return full file name.
 */
char *get_file_name(char *file_name,char *p, int addr){
    
    char *ext = (char *)malloc(sizeof(char));
    for(int i =0; i < 8; i++){
        if(p[addr+i] == ' '){
            i++;
            continue;}
        file_name[i] = p[addr+i];
    }   
    for(int j = 8 ; j < 12 ; j++){
        if(p[addr+j] == ' '){
            j++;
            continue;}
        ext[j-8]=p[addr+j];
    }
    file_name = concatenate(file_name,ext);
    free(ext);
    return file_name;
}

/**
 * @brief Get the size of argument file.
 * 
 * @param p Image pointer.
 * @return int size of file.
 */
int get_size(char *p){

    return ((p[28]&0xff)+((p[29]&0xff)<<8)+((p[30]&0xff)<<16)+((p[31]&0xff)<<24));
}

/**
 * 
 * @param p Image pointer.
 * @param dsr_file file that we looking for.
 * @return The directories of this file.
 */
int search_file(char *p, char *dsr_file){
    int addr = 0x2600;
    char *file_name = (char *)malloc(sizeof(char));
	while(addr < 33*512 && p[0]!= 0x00){
    	
    	file_name = get_file_name(file_name,p,addr);
        
    	if(strcmp(file_name, dsr_file) == 0){ 
            free(file_name);
    		return addr;
    	}
   		addr += 32;
    }
    free(file_name);
    return 0;
}
/**
 * @brief converting the file name to all uppercase letters.
 * 
 * @param arg file name.
 * @return file name with all uppercase letters.
 */
char *convert_to_upper(char *arg){
    char *upper = arg;
    int i = 0;
    while(upper[i]){
        upper[i] = toupper(upper[i]);
        i++;
    }
    return upper;
}

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

/**
 * @brief write the file into current path.
 * 
 * @param first_logical_num 26th offset with length of 2 bytes.
 * @param file_size the size of file we looking for.
 * @param dsr_file  the name of file.
 * @param p Image pointer.
 */
void put_file(int first_logical_num,int file_size,char *dsr_file,char *p){
    FILE *dest = fopen(dsr_file,"wb");
    int next_fat = get_fat_val(first_logical_num,p);
    int addr = (first_logical_num+31)*512;
    int update = 0;
    while(next_fat != LAST_CLUSTER){
        
        if(update!= 0 ){
            addr = (update + 31) * 512;
        }
        for( int i = 0 ; i < 512 ; i++){
            fputc(p[addr + i],dest);
        }
    
        update = next_fat;
        next_fat = get_fat_val(next_fat,p);
        
    }
    addr = (update+31)*512;

   
    for (int j = 0; j<(file_size - (file_size/512)*512); j++){
        fputc(p[addr + j],dest);
    }
    fclose(dest);
}

int main(int argc, char *argv[]){
    int fd = open(argv[1],O_RDWR);
    struct stat buffer;
    int status = fstat(fd,&buffer);
    if(argv[2] == NULL){
        fprintf(stderr,"Usage : ./disk_get <Image> <filename>\n");
        exit(1);
    }
    if(status != 0){
        fprintf(stderr,"File image status error.\n");
        exit(1);
    }
    char *p = mmap(NULL, buffer.st_size, PROT_READ | PROT_WRITE, MAP_SHARED, fd, 0); 
    if (p == MAP_FAILED) {
		printf("Error: failed to map memory\n");
		exit(1);
	}
    char *dsr_file = convert_to_upper(argv[2]);

    int flag = 0;
    flag = search_file(p,dsr_file);
    
    if(flag != 0){
        
        int first_logical_num =p[flag+26]+(p[flag+27]<<8);
        int file_size = (p[flag+28]&0xff)+((p[flag+29]&0xff)<<8)+((p[flag+30]&0xff)<<16)+((p[flag+31]&0xff)<<24);
        
        
        put_file(first_logical_num,file_size,dsr_file,p);
    }
    else{
        printf("File is not found.\n");
    }
    munmap(p, buffer.st_size);
    close(fd);
    return 0;
}
