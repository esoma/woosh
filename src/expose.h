#ifndef WOOSH_PUBLIC_H
#define WOOSH_PUBLIC_H

#if defined _WIN32 || defined __CYGWIN__
    #define WOOSH_EXPOSE
#else
    #define WOOSH_EXPOSE __attribute__ ((visibility ("default")))
#endif

#endif