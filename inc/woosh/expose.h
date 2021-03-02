#ifndef WOOSH_PUBLIC_H
#define WOOSH_PUBLIC_H

#if defined _WIN32 || defined __CYGWIN__
    #ifdef WOOSH_EXPORT
        #define WOOSH_EXPOSE_ __declspec(dllexport)
    #else
        #define WOOSH_EXPOSE_ __declspec(dllimport)
    #endif
#else
#ifdef WOOSH_EXPORT
    #define WOOSH_EXPOSE_ __attribute__ ((visibility ("default")))
#else
    #define WOOSH_EXPOSE_
#endif
#endif

#endif
