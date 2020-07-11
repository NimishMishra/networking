# Leviathan walkthrough

Host: leviathan.labs.overthewire.org
Port: 2223

Submitting on wechall:
`WECHALLUSER="username" WECHALLTOKEN="token" wechall`

# Level 0

URL: ```ssh leviathan0@leviathan.labs.overthewire.org -p 2223```

On close investigation using `-ls la`, there's a directory `.backup` storing the password. A simple `cat bookmarks.html | grep password` does the trick

Password: rioGegei8m

# Level 1

## Decompiling a binary

URL: ```ssh leviathan1@leviathan.labs.overthewire.org -p 2223```

Have a look at how binary files are organised [here](https://www.akashtrehan.com/different-kinds-of-executables/)

Amidst loads of information, the file `./check` is non-stripped, implying it has some debugging information. Thus, we fire `ltrace ./check` `ltrace` has the following:

```s
ltrace is a program that simply runs the specified command until it exits. It intercepts and records the dynamic library calls which are called by the executed process and the signals which are received by that process. It can also intercept and print the system calls executed by the program.
```

On running `ltrace`, there's a point where `strcmp(__input__, "sex")` which is the `strcmp` for password. Thus `sex` is the password the this `setuid`. Once run, privileges are escalted and then a simple `cat /etc/leviathan_pass/leviathan2` does the trick.

Password: ougahZi8Ta

# Level 2

URL: ```ssh leviathan2@leviathan.labs.overthewire.org -p 2223```


ltrace output: (line in 342-344)

__libc_start_main(0x804852b, 2, 0xffffd764, 0x8048610 <unfinished ...>