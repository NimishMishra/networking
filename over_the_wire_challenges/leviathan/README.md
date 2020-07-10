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

URL: ```ssh leviathan1@leviathan.labs.overthewire.org -p 2223```

