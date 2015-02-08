# gotdid
Another todo list, with emphasis on did. For people who like simple.

I like toto lists but never found a good way to keep track of things I want to do in a coding activity. Using TODO tags in comments is ok. Lots of things you want to do aren't things that make sense trapped in code comments. I haven't found any great personal tool and the kinds of todo items I want to keep track of don't seem like something to clutter up a bug database (or set one up).

I want something low friction right were I am likely to be - checking out files from a git or hg repo. Even better if it workid kinda like, and maybe with version control. 

Searching internet I found this tool by stevelosh.com/projects/t. I really liked the simplicity and the author's preference for getting stuff done over keeping track of things. It was almost what I wanted but I usually work in Windows and I want to use Python more and I want a few more features so I made my own tool to share.

I like to use this tool right in the repo. I create a todo file in the root folder of the repo and keep all my todo items right there. When it is time to commit I can, if I choose, check in the .gotdid file and use my version control as my backup. No matter where I am in the folder tree the gotdid script looks up the tree for the .gotdid file so it works like your Hg does. 
