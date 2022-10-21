#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <signal.h>
#include <sys/wait.h>
#include <sys/types.h>
#include <unistd.h>
/**
 * @brief define a node struct for saving information of processes into linked list.
 * 
 */
typedef struct Node
{
    pid_t pid;
    // char *path;
    char path[128];
    struct Node *next;
} node;

node *head = NULL; // initial list.

/**
 * @brief save new process information as a node into linked list.
 * 
 * @param new_pid the pid of new process that fork by bg.
 * @param new_path the path/process name of new process that fork by bg. 
 */
void add_new_Node(pid_t new_pid, char *new_path)
{
    node *new_node = (node *)malloc(sizeof(node));
    new_node->pid = new_pid;

    strcpy(new_node->path, new_path);
    new_node->next = NULL;

    if (head == NULL)
    {
        head = new_node;
    } // new list created.
    else
    {
        node *tmp = head;
        while (tmp->next != NULL)
        {
            tmp = tmp->next;
        }
        tmp->next = new_node;
    } // existing list.
}

/**
 * @brief delete node existing in list, if node not found, error message generated.
 * 
 * @param pid the pid of process that to be deleted.
 */
void delete_Node(pid_t pid)
{
    if (pid == head->pid)
    { // only one node exist in list.
        if (head->next == NULL)
        {
            head = NULL;
            free(head);
        }
        else
        {
            head = head->next;
        }
    }
    else
    { // more nodes in list.
        node *tmp = head;
        int flag = false;
        while (tmp != NULL && tmp->pid != pid)
        {
            tmp = tmp->next;
            if (tmp->pid == pid)
            {
                free(tmp);
                flag = true;
            }
        }
        if (flag == false)
        {
            fprintf(stderr, "Invilid pid, process not found.\n");
        }//process not found.
    }
}

/**
 * @brief check if process existing in list by traversal the whole list from head node.
 * 
 * @param pid the pid of the process to be reviewed.
 * @return int boolean value,if process exists in list return true; otherwise return false.
 */
int PifExist(pid_t pid)
{
    node *tmp = head;

    while (tmp != NULL)
    {
        if (tmp->pid == pid)
        {
            return true;
        }
        tmp = tmp->next;
    }
    return false;
}

/**
 * @brief create and execute a background process by calling fork() and execvp().
 * If fork fail, an error message will be sent to terminal.
 * 
 * @param input usage: bg <process>.
 */
void bg(char **input)
{
    pid_t pid;
    pid = fork();
    if (pid == 0)
    {
        char *cmd = input[1];
        execvp(cmd, &input[1]);
        printf("PMan: Child process finished (fork may fail due to process).\n"); // exception handling.
        printf("Pman: > ");
        exit(false);
    }
    else if (pid > 0)
    {
        printf("Background process now starting with pid : %d\n", pid);
        add_new_Node(pid, input[1]);
    }
    else
    {
        perror("\nFail to create a new process.\n");
        exit(1);
    }
}
/**
 * @brief print all processes that recorded by bg, then count the numbers of process.
 * 
 * @param input usage : bglist
 */
void bglist(char **input)
{
    int count = 0;
    node *tmp = head;
    while (tmp != NULL)
    {
        printf("%d:\t./%s \n", tmp->pid, tmp->path);
        tmp = tmp->next;
        count++;
    }
    printf("Total background jobs:  %d\n", count);
}

/**
 * @brief send a kill signal to specific process by input pid. 
 * If pid not found, error message will be printed.
 * 
 * @param str_pid input pid.
 */
void bgkill(char *str_pid)
{
    int pid = atoi(str_pid);
    int flag = true;
    if (!PifExist(pid))
    {
        fprintf(stderr, "invalid pid.\n");
        flag = false;
    }
    if (flag == true)
    {
        kill(pid, SIGTERM);
    }
}
/**
 * @brief send a stop signal to specific process by input pid. 
 * If pid not found, error message will be printed.
 * 
 * @param str_pid input pid.
 */
void bgstop(char *str_pid)
{
    int pid = atoi(str_pid);
    int flag = true;
    if (!PifExist(pid))
    {
        fprintf(stderr, "invalid pid.\n");
        flag = false;
    }
    if (flag == true)
    {
        kill(pid, SIGSTOP);
    }
}

/**
 * @brief send a start signal to specific process by input pid. 
 * If pid not found, error message will be printed.
 * 
 * @param str_pid input pid.
 */
void bgstart(char *str_pid)
{
    int pid = atoi(str_pid);
    int flag = true;
    if (!PifExist(pid))
    {
        fprintf(stderr, "invalid pid.\n");
        flag = false;
    }
    if (flag == true)
    {
        kill(pid, SIGCONT);
    }
}
/**
 * @brief receive the status of specific process, and print the fields by order.
 * #####[The values of utime & stime still need to be debugged.]#####
 * 
 * @param str_pid input pid.
 */
void pstat(char *str_pid)
{
    pid_t pid = atoi(str_pid);

    if (!PifExist(pid))
    {
        fprintf(stderr, "Process %d does not exist.\n", pid);
        exit(false);
    }
    else
    {
        int id;
        char filename[1000];
        char comm[1000];
        char state;
        long double utime, stime;
        long int rss;

        sprintf(filename, "/proc/%d/stat", pid);
        FILE *fp = fopen(filename, "r");
        if (fp == NULL)
        {
            fprintf(stderr, "Cannot open file.\n");
            exit(false);
        } // input check.
        fscanf(fp, "%d %s %c %Lf %Lf %ld", &id, comm, &state, &utime, &stime, &rss);
        printf("comm:\t%s\n", comm);
        printf("state:\t%c\n", state);
        printf("utime:\t%Lf\n", (utime / sysconf(_SC_CLK_TCK)));
        printf("stime:\t%Lf\n", (stime / sysconf(_SC_CLK_TCK)));
        printf("rss:\t%ld\n", rss);
        fclose(fp);
    }
}

/**
 * @brief main function from help code in brightspace.
 * 
 * @return int normal exit.
 */
int main()
{
    char user_input_str[50];
    
    while (true)
    {
        
       
        printf("Pman: > ");
        fgets(user_input_str, 50, stdin);
        char *ptr = strtok(user_input_str, " \n");
        if (ptr == NULL)
        {
            continue;
        }
        char *lst[128];
        int index = 0;
        lst[index] = ptr;
        index++;
        while (ptr != NULL)
        {
            ptr = strtok(NULL, " \n");
            lst[index] = ptr;
            index++;
        }
        if (strcmp("bg", lst[0]) == 0)
        {
            bg(lst);
        }
        else if (strcmp("bglist", lst[0]) == 0)
        {
            bglist(lst);
        }
        else if (strcmp("bgkill", lst[0]) == 0)
        {
            bgkill(lst[1]);
        }
        else if (strcmp("bgstop", lst[0]) == 0)
        {
            bgstop(lst[1]);
        }
        else if (strcmp("bgstart", lst[0]) == 0)
        {
            bgstart(lst[1]);
        }
        else if (strcmp("pstat", lst[0]) == 0)
        {
            pstat(lst[1]);
        }
        else if (strcmp("q", lst[0]) == 0)
        {
            printf("Bye Bye \n");
            exit(0);
        }
        else
        {
            printf("PMan: > %s:  command not found.\n", user_input_str);
        }
    }

    return 0;
}