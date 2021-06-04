#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <sys/types.h>
#include <sys/inotify.h>
#include <limits.h>
#include<sys/stat.h>
#include<dirent.h>
#include<time.h>
#include<string.h>
#include<unistd.h>

#define MAX_EVENTS 1024 /*Max. number of events to process at one go*/
#define LEN_NAME 16 /*Assuming that the length of the filename won't exceed 16 bytes*/
#define EVENT_SIZE  ( sizeof (struct inotify_event) ) /*size of one event*/
#define BUF_LEN     ( MAX_EVENTS * ( EVENT_SIZE + LEN_NAME )) /*buffer to store the data of events*/

void monitor(char *);
int evnt_mon(char *); 




void main()
{
    if(fork()==0)
    evnt_mon("./usssb");// give path of your directory which you want to monitor
    monitor("./usssb");// give path of your directory which you want to monitor
    while(1);
}

void monitor(char * rt_dir)
{

    struct stat st;
    DIR *dirp; 
    struct dirent *dp;
    char str[100][100]={ };
    char temp[100];
    char str1[500]=" ";
    int i=0,j=0,src_ret=9,src_ret1=9;
    strcpy(str1,rt_dir);
    dirp=opendir(str1);
    if(dirp==NULL)
    {
        perror("opendir");
        return;
    }

    while(1)
    {
        dp=readdir(dirp);
        if(dp==NULL)
        break;
        if((strcmp(dp->d_name,".\0")==0) || (strcmp(dp->d_name,"..")==0))
        continue;   

        if((dp->d_type==DT_DIR)&&((strcmp(dp->d_name,".")!=0)&&(strcmp(dp->d_name,"..")!=0)))
        {   
            strcat(str[i],str1);
            strcat(str[i],"/");
            strcat(str[i],dp->d_name);
            if(fork()==0)   
            {
                evnt_mon(str[i]);
            }
            i++;
        }

    }

    closedir(dirp);
    if(i>0)
    {
        for(j=0;j<i;j++)
        {
            monitor(str[j]);    
        }
    }

}




int evnt_mon(char *argv) 
{
    int length, i = 0, wd;
    int fd;
    char buffer[BUF_LEN];

    /* Initialize Inotify*/
    fd = inotify_init();
    if ( fd < 0 )
    {
        perror( "Couldn't initialize inotify");
    }

    /* add watch to starting directory */
    wd = inotify_add_watch(fd, argv, IN_CREATE | IN_MODIFY | IN_DELETE); 

    if (wd == -1)
    {
        printf("Couldn't add watch to %s\n",argv);
    }
    else
    {
        printf("Watching:: %s\n",argv);
    }

    /* do it forever*/
    while(1)
    {
        i = 0;
        length = read( fd, buffer, BUF_LEN );  
        if ( length < 0 )
        {
            perror( "read" );
        }  

        while ( i < length )
        {
            struct inotify_event *event = ( struct inotify_event * ) &buffer[ i ];
            if ( event->len )
            {
                if ( event->mask & IN_CREATE)
                {
                    if (event->mask & IN_ISDIR)
                    {
                        printf( "The directory %s was Created in %s.\n", event->name,argv );    


                        if(fork()==0)
                        {
                            char p[100]=" ";
                            strcpy(p,argv);
                            strcat(p,"/");
                            strcat(p,event->name);
                            evnt_mon(p);
                        }

                    }                       
                    else
                            printf( "The file %s was Created with WD %d\n", event->name, event->wd );       
                    }

                    if ( event->mask & IN_MODIFY)
                {
                            if (event->mask & IN_ISDIR)
                            printf( "The directory %s was modified.\n", event->name );       
                            else
                            printf( "The file %s was modified with WD %d\n", event->name, event->wd );       
                    }

                    if ( event->mask & IN_DELETE)
                {
                            if (event->mask & IN_ISDIR)
                            printf( "The directory %s was deleted from %s.\n", event->name,argv );       
                            else
                            printf( "The file %s was deleted with WD %d\n", event->name, event->wd );       
                    }  

                i += EVENT_SIZE + event->len;
            }
            }
        }

    /* Clean up*/
    inotify_rm_watch( fd, wd );
    close( fd );

    return 0;
}
