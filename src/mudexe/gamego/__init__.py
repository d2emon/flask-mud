"""
Two Phase Game System
extern FILE *openlock();
char **argv_p;
char privs[4];
"""


# ???
pr_due = False


def crapup(s):
    global pr_due

    dashes = "\n-" + "=-" * 38
    # pbfr();
    pr_due = 0  # So we dont get a prompt after the exit
    print("%s\n\n%s\n%s" % (dashes, s, dashes))
    exit(0)


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


def set_progname(n, text):
    """
    /*
    int x=0;
    int y=strlen(argv_p[n])+strlen(argv_p[1]);
    y++;
    if(strcmp(argv_p[n],text)==0) return;

    while(x<y)
        argv_p[n][x++]=0;
    strcpy(argv_p[n],text);
    */
    """
