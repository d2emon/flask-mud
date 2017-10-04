"""

B functions and utilities

"""
# from .global_vars import logger
from .world_file import WorldFile
# include <stdio.h>
# include <pwd.h>

# include <ctype.h>
# include "System.h"


def lowercase(stri):
    """
    char *stp=str;
    while(*str)
    {
        if(isupper(*str)) *str=tolower(*str);
        str++;
    }
    return(stp);
    """


def uppercase(stri):
    """
    char *stp=str;
    while(*str)
    {
        if(islower(*str)) *str=toupper(*str);
        str++;
    }
    return(stp);
    """


def trim(stri):
    """
    char *x;
    x=str+strlen(str);
    while(*x==32)
    {
        *x=0;
        x--;
    }
    return(str);
    """


def any(ch, stri):
    """
    extern char *strchr();
    if(strchr(str,ch)==NULL) return(-1);
    return(strchr(str,ch)-str);
    """


def gepass(stri):
    """
    char key[33],pw[16];

    strcpy(key,getpass(""));
    strcpy(pw,crypt(key,"XX"));
    strcpy(str,pw);
    """


def scan(cout, cin, cstart, cskips, cstops):
    """
    char *in_base=in;
    /*	char *sy_ot=out;
        printf("Scan(%s ->%d %d %s %s",in,out,start,skips,stops);*/
    if(strlen(in)<start) {*out=0;return(-1);}
    in+=start;
    while((*in)&&(strchr(skips,*in))) in++;
    if(*in==0) {*out=0;return(-1);}
    while((*in)&&(strchr(stops,*in)==0))
    {
        *out= *in;
        out++;
        in++;
    }
    /*	printf(" : Outputting %s\n",sy_ot); */
    *out=0;
    return(in-in_base);
    """


def getstr(f, st):
    """
    extern char *strchr();
    if(!fgets(st,255,file)) return(0);
    if(strchr(st,'\n')) *strchr(st,'\n')=0;
    return(st);
    """


def addchar(stri, ch):
    """
    int x=strlen(str);
    str[x]=ch;
    str[x+1]=0;
    """


def numarg(stri):
    """
    long i=0;
    sscanf(str," %ld",&i);
    return(i);
    """


def sbar():
    return -1  # Unknown code needed here


def f_listfl(name, f):
    """
    FILE *a;
    char x[128];
    a=fopen(name,"r");
    if(a==NULL) fprintf(stderr,"[Cannot find file ->%s ]\n",name);
    else
    {
        while(fgets(x,127,a)) fprintf(file,"%s",x);
    }
    """


SIZE_OF_LONG = 4


def sec_read(unit, block, pos, l):
    """
    """
    wf = WorldFile()
    wf.open(unit)
    wf.seek(pos)
    block = wf.sec_read(l)


def sec_write(unit, block, pos, l):
    """
    """
    wf = WorldFile()
    wf.open(unit)
    wf.seek(pos)
    wf.sec_write(block, l)


def cuserid(stri):
    """
    /*
        extern char *strchr();
        getpw(getuid(),ary);
        *strchr(ary,':')=0;
    */
    static char ary[128];
    strcpy(ary,getpwuid(getuid())->pw_name);
    if(str!=NULL) strcpy(str,ary);
    return(ary);
    """
