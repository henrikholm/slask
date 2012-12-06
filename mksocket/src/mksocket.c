#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <errno.h>
#include <string.h>
#include <sys/types.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <argp.h>
#include <signal.h>
#include <unistd.h>


//--------------------------------------------------
//
//  DEFINES
//
//--------------------------------------------------
#define BUF_SZ 1024



//--------------------------------------------------
//
//  DECLARATIONS
//
//--------------------------------------------------
void ex_program(int sig);
void cleanup(void);
static error_t parse_opt (int key, char *arg, struct argp_state *state);



//--------------------------------------------------
//
//  GLOBALS
//
//--------------------------------------------------
const char *argp_program_version = "mksock 1.0";
const char *argp_program_bug_address = "<henrik.holm@me.com>";

static char doc[] = "\nmksock -- A program to create a socket and print in terminal everything that is sent to it.\n";
static char args_doc[] = "SOCKET - Name and path to the socket";

static int sockfd; // File descriptor for socket.
static int sockfd_fork; // This is the forked socket returned from 'accept', only used in stream-mode

struct arguments {
    char *args[1];          // ARG1 - Path to the socket
    int stream;             // The -s flag, use SOCK_STREAM
    int follow;             // The -f flag, keep the socket open
};

static struct argp_option options[] = {
    {"stream", 's', 0, 0, "Connect socket as a stream instead of datagram (default)"},
    {"follow", 'f', 0, 0, "Keep the socket open and output all data sent to it"},
    {0}
};

static struct argp argp = {options, parse_opt, args_doc, doc};
static struct arguments arguments;



//--------------------------------------------------
//
//  MAIN
//
//--------------------------------------------------
int main(int argc, char *argv[]) {

    int32_t sock_type;                      // Holds what kind of socket; DGRAM / STREAM
    uint32_t addr_sz, recv_sz;              // Size of socket address and recieved packet
    struct sockaddr_un local, remote;       // Address structures of local and remote socket
    char str[BUF_SZ];                       // Message buffer

    // Default values
    arguments.stream = 0;
    arguments.follow = 0;

    // Register signal handler, i.e handle "Ctrl-c" and such
    (void) signal(SIGINT, ex_program);

    argp_parse (&argp, argc, argv, 0, 0, &arguments);

    // Create the socket as a dgram or as a stream
    if(arguments.stream){
        sock_type = SOCK_STREAM;
    } else {
        sock_type = SOCK_DGRAM;
    }

    // Create the socket
    if ((sockfd = socket(AF_UNIX, sock_type, 0)) == -1) {
        perror("socket");
        exit(1);
    }

    // Copy path over to the sockaddr structure
    local.sun_family = AF_UNIX;
    strcpy(local.sun_path, arguments.args[0]);
    addr_sz = strlen(local.sun_path) + sizeof(local.sun_family);

    // Bind the socket to the path
    if (bind(sockfd, (struct sockaddr *)&local, addr_sz) == -1) {
        perror("bind");
        cleanup();
        exit(1);
    }

    if (arguments.stream){
    //
    //  Stream routines
    //
        if (listen(sockfd, 5) == -1) {
            perror("listen");
            cleanup();
            exit(1);
        }

        printf("Waiting for stream on socket '%s'\n", local.sun_path);

        // Hang in the 'accept' method until we recieve a connection
        if ((sockfd_fork = accept(sockfd, (struct sockaddr *)&remote, &addr_sz)) == -1) {
            perror("accept");
            cleanup();
            exit(1);
        }

        do {
            recv_sz = recv(sockfd_fork, str, BUF_SZ, 0);

            if (recv_sz == 0){
                printf("Got empty data stream from client, hanging up.\n");
                break;

            } else if (recv_sz < 0) {
                perror("recv");
                cleanup();
                exit(1);

            } else {
                // Print what we recieved
                printf("%s\n", str);
            }

        } while (arguments.follow);

    } else {
    //
    //  Datagram routines
    //
        printf("Waiting for datagram on socket '%s'\n", local.sun_path);

        do {
            if (read(sockfd, str, BUF_SZ) < 0){
                perror("receiving datagram packet");
                cleanup();
                exit(1);
            }

            printf("%s\n", str);

        } while (arguments.follow);

    }

    cleanup();

    return 0;

}


//--------------------------------------------------
//
//  HELPER FUNCTIONS
//
//--------------------------------------------------
static error_t parse_opt (int key, char *arg, struct argp_state *state) {
    struct arguments *arguments = state->input;

    switch (key) {
        case 's':
            arguments->stream = 1;
            break;
        case 'f':
            arguments->follow = 1;
            break;
        case ARGP_KEY_ARG:
            if (state->arg_num >= 1) {
                argp_usage(state);
            }
            arguments->args[state->arg_num] = arg;
            break;
        case ARGP_KEY_END:
            if (state->arg_num < 1) {
                argp_usage (state);
            }
            break;
        default:
            return ARGP_ERR_UNKNOWN;
    }
        return 0;
}

void cleanup(void){

    unlink(arguments.args[0]);
    close(sockfd);
    close(sockfd_fork);

}

void ex_program(int sig) {

    printf("Exit on signal - %d\n", sig);
    cleanup();
    (void) signal(SIGINT, SIG_DFL);
}