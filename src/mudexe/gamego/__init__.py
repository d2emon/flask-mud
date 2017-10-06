"""
Two Phase Game System
extern FILE *openlock();
char privs[4];
"""


def listfl(name):
    """
    FILE *a;
    char b[128];
    a=openlock(name,"r+");
    while(fgets(b,128,a)) printf("%s\n",b);
    fcloselock(a);
    """


def getkbd(s, l):
    """
    char *getkbd(s,l)   /* Getstr() with length limit and filter ctrl */
    char *s;
    int l;
    {
    char c,f,n;
    f=0;c=0;
    while(c<l)
    {
        regec:n=getchar();
        if ((n<' ')&&(n!='\n')) goto regec;
        if (n=='\n') {s[c]=0;f=1;c=l-1;}
        else
            s[c]=n;
        c++;
    }
    if (f==0) {s[c]=0;while(getchar()!='\n');}
    return(s);
    }
    """
