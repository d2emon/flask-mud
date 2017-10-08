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
