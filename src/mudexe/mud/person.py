def delpers(name):
    """
    {
    FILE *i;
    PERSONA x;
    l1:
    i=(FILE *)personactl(name,&x,PCTL_FIND);
    if(i==(FILE *)-1) return;
    lowercase(name);
    lowercase(x.p_name);
    if(strcmp(x.p_name,name))
        crapup("Panic: Invalid Persona Delete");
    strcpy(x.p_name,"");
    x.p_level= -1;
    fwrite(&x,sizeof(PERSONA),1,i);
    fcloselock(i);
    goto l1;
    }
    """


def saveme():
    """
    extern char globme[];
    extern long zapped;
    PERSONA x;
    extern int mynum;
    strcpy(x.p_name,globme);
    x.p_strength=my_str;
    x.p_level=my_lev;
    x.p_sex=psexall(mynum);
    x.p_score=my_sco;
    if(zapped) return;
    bprintf("\nSaving %s\n",globme);
    putpers(globme,&x);
    """


def validname(name):
    """
 char *name;
    {
    long a;
    if(resword(name)){bprintf("Sorry I cant call you that\n");return(0);  }
    if(strlen(name)>10)
       {
       return(0);
       }
    a=0;
    while(name[a])
       {
       if(name[a]==' ')
          {
          return(0);
          }
       a++;
       }
    if(fobn(name)!=-1)
       {
      bprintf("I can't call you that , It would be confused with an object\n");
       return(0);
       }
    return(1);
    }
    """


def resword(name):
    """
{
if(!strcmp(name,"The")) return(1);
if(!strcmp(name,"Me")) return(1);
if(!strcmp(name,"Myself")) return(1);
if(!strcmp(name,"It")) return(1);
if(!strcmp(name,"Them")) return(1);
if(!strcmp(name,"Him")) return(1);
if(!strcmp(name,"Her")) return(1);
if(!strcmp(name,"Someone")) return(1);
return(0);
}
    """
