#include <iostream>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <netinet/in.h>
#include <netdb.h>

/* compile:
 *    g++ workerClient.cpp -o workerclient
 */


void RunWorkerWorker();
bool ProcessReceivedMessage(char buffer [], int size, int sockfd);
void ComputeRandomNumber(int sockfd);

void error(char *msg) {
    perror(msg);
    exit(1);
}


int main() {
    RunWorkerWorker();
    return 0;
}

void RunWorkerWorker() {
    const char SERVER [] = "localhost";
    const int SERVER_PORT = 8005;
    
    int sockfd, n;
    const int BUFFER_SIZE = 1024;
    char buffer[BUFFER_SIZE];
    struct sockaddr_in serv_addr;
    struct hostent *server;

    printf("[Running Worker...]\n");
    fflush(stdout);

    /* Set up socket stuff */
    sockfd = socket(AF_INET, SOCK_STREAM, 0);
    if (sockfd < 0){
        error("[Worker] ERROR opening socket");
        printf("[Worker] ERROR opening socket");
        fflush(stdout);
    }
    
    server = gethostbyname(SERVER);
    if (server == NULL) {
        fprintf(stderr,"[Worker] ERROR, no such host\n");
        printf("[Worker] ERROR, no such host\n");
        exit(0);
    }
    
    bzero((char *) &serv_addr, sizeof(serv_addr));
    
    serv_addr.sin_family = AF_INET;
    
    bcopy((char *)server->h_addr,
         (char *)&serv_addr.sin_addr.s_addr,
         server->h_length);
    
    serv_addr.sin_port = htons(SERVER_PORT);
    
    /* Try to connect to server listening on host/port */
    if (connect(sockfd,(struct sockaddr*)&serv_addr,sizeof(serv_addr)) < 0){
        error("[Worker] ERROR connecting");
        printf("[Worker] ERROR connecting\n");
        fflush(stdout);
    }


    bzero(buffer,BUFFER_SIZE);
    
    /*
    sprintf(buffer, "bonjour! i am the client!\r\n");
    n = write(sockfd,buffer,strlen(buffer));
    if (n < 0)
         error("[Worker] ERROR writing to socket");
    bzero(buffer,BUFFER_SIZE);
    n = read(sockfd,buffer,BUFFER_SIZE-1);
    if (n < 0)
        error("[Worker] ERROR reading from socket");
        
    printf("%s\n",buffer);

    if (strncmp(buffer, "Denied", strlen("Denied")) == 0)
        exit(0);

    bzero(buffer,BUFFER_SIZE);
    */

    bool shutdown = false;
    
    while(read(sockfd,buffer,BUFFER_SIZE-1) && !shutdown){
        shutdown = ProcessReceivedMessage(buffer, BUFFER_SIZE-1, sockfd);
    }

    printf("[Worker]  Shutting down...\n");
}

bool ProcessReceivedMessage(char buffer [], int size, int sockfd)
{
    printf("[ProcessReceivedMessage] Received message: %s\n", buffer);
    fflush(stdout);

    int n;

    /* Parse the command */
    if (strncmp(buffer, "random ", strlen("random")) == 0) {
        printf("Received command to generate random number!\n");
        ComputeRandomNumber(sockfd);
    }
    else if (strncmp(buffer, "shutdown ", strlen("shutdown")) == 0){
        printf("Received SHUTDOWN command.\n");
        return true;
    }   

    fflush(stdout);
    return false;

}

void ComputeRandomNumber(int sockfd)
{
    char ret_str[1024];
    sprintf(ret_str,
            "{ 'random_number': %d }\r\n", rand());
    int n = write(sockfd, ret_str, strlen(ret_str));
    if (n < 0)
         error("[Worker] ERROR writing to socket");
}
