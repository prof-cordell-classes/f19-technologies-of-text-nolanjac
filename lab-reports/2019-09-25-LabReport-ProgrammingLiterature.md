# Lab Report: Programming Literature

#### JACK NOLAN

## Process Description

This lab, we made Twitter bots! This worked by carefully arranging strings in a JSON file, so that they can generate a random message. We used [Tracery](http://tracery.io/) to test our JSON files, and published our bots using [Cheap Bots, Down Quick](https://cheapbotsdonequick.com/).

In order to "program" our bots we created JSON files. These were arranged with the "origin" line containing the highest level information, with further words getting selected by words between # symbols like so: #action#, which would choose a random string from the "action" line in the JSON. You can also set basic variables, which are set to a random string of your selected categories but can then be used multiple times throughout the tweet. I used this so I could get all of the different people in the poems consistent across all of the lines of the poem.

My Twitter Bot can be found [here](https://twitter.com/TechnologiesBot).
The JSON source can be found in the `twitterBot.json` file in the same folder as this lab report.

## Observations

Although this wasn't a particularly difficult activity understand, it still wasn't actually all that intuitive to accomplish. For example, there were multiple times when I had my bot fully written, and then in testing it, I would need to debug until I removed some whitespace characters or other things which should not even affect the JSON when it gets parsed. Also, *Tracery* would not create a new line for `\n` characters, even though *Cheap Bots, Done Quick* did correctly. Anyway, despite all of its issues, *Tracery*, was actually a great tool to use once you got things working because it would show you graphically how your tweets were getting built, which was very convenient for making them more complex. You could see which words were coming from which lines, and what data was coming from a variable or getting generated randomly. This all made debugging the grammar issues my bot would generate much easier and made the tweets flow much better.

Also, I was surprised by the flexibility you could get with the JSON scheme we were using. As long as you wanted your text to follow some general pattern, you could make your bot generate as complex of text as you could want, as long as you're were clever enough. I was originally going to complain about all of its limitations, but I have since realized that I could have overcome most of them. As an example, while something like "I read" is good grammar, something like "Alexander Hamilton read" is not. While writing my bot, I simply could not find a way to make "read" into "reads" depending on the first word, so instead I just removed all of the options until the person section only contained "I" and "you", and then put all of the other people and names into a different category of people to be used in other parts of the poem. Now, as I am writing this lab report, I have realized I actually could have solved that problem if I had made a category of `#personAction#` which pointed to `{"#IYou# read", "#OtherPerson# reads"}`, so that all of the sentences would be grammatically correct. Of course, other challenging problems like linking multiple tweets together or reading some data from the outside world would not be possible with this technology, but that's okay because this is meant to be a simple system to use.

## Analysis

With computers becoming such a fundamental element in many people's daily lives, it becomes relevant for your everyday person to understand them to a greater degree. Not just how to use them, but, on a basic level, how they function at all. Making Twitter bots is a great activity for this. Even though our JSON-based Twitter bots could not do everything, like counting or adding numbers, you could still create complex posts using its simple design if you are creative enough. This is what is at the heart of all programming, circumnavigating your limitations and solving your problems creatively. Programming is always a creative endeavor used to solve some sort of problem; even if that problem is "how can I make a funny twitter bot"? Learning how computers work at some basic level does not require any understanding of how all of the different pieces of hardware interact in your computer or knowledge of any programming languages. Programming is more fundamental than that; it is a problem-solving tool. It allows you to merge logic and creativity to find solutions to any arbitrary problem, not just those on the computer.

This is why programming is an important literacy, because it's such a useful tool, applicable to so many different situations. And, as Annette Vee points out in her introduction to *Coding Literacy: How Computer Programming is Changing Writing*, programming has not existed long enough and has not been used by enough people to truly show how useful a tool it could be. Just like it was hard to imagine a world where everyone was illiterate just a couple hundred years ago, perhaps in a couple dozen years, we will feel the same way about coding. Coding poetic Twitter bots is such a small slice of the creative, artistic, useful, utilitarian programming creations. There are so many possibilities, especially with the sheer number and type of computers quietly working along out there, that it is hard to imagine the benefits that could come from an increased literacy in programming.

In the last lab report for Markdown, I discussed extensively about whether a website could be considered a "book" and what the ramifications of such a classification would be. After reading the first chapter, "The Book as Object", from *The Book*, by Amaranth Borsuk, it may be worthwhile to continue that discussion. Surely, a website must be considered a "book as content" because the content of websites and books are so similar, but a website "as an object"? After following the technological progress in the book, as laid out by Borsuk, the digital book, the website, seems like the obvious next step in the book's evolution. The history of the book is a history of increasing interactivity with the reader and the website (not necessarily ebooks) falls perfectly into that tradition. What first started on cuneiform tablets, the least interactive medium, changed to the scroll, a more interactive medium as you can roll around to the sections you are interested in, and finally evolved into the codex, which even more interactive in that you can flip directly to the page you want and you don't need to rewind when you finish the book. The pages of a codex can be flipped through quickly or skimmed for items of interest or read slowly, one page at a time. This is as a result of the book as an object. The website also achieves an advancement in this regard. The different pages of a website can often be explored with ease and speed, scanned quickly for headlines which catch your eye, or perused slowly and carefully. The website is still a physical kind of experience - you must move your hands to interact with it, to move the mouse or touch the screen - there is still light coming off a physical object, your computer, and entering your eyes. Even in size it follows the trend from thick blocks of clay, to rolled up parchment, to square books, to a bit of space on a hard drive. Each book is slightly more space efficient than the last, ending with the website, taking up only a tiny bit of physical space, often hundreds of miles away from where you access it. It's an amazing thing.



----

### A Collection of my favorite tweets thus far:

> And what you shriek at, Alexander Hamilton shall shriek at.

[tweet](https://twitter.com/TechnologiesBot/status/1176840735049564160)

> I shriek at myself, and absorb the powers of myself.

[tweet](https://twitter.com/TechnologiesBot/status/1175391194471419906)

> I know your cat, and consume your cat,
I cower before your cat, and absorb the powers of your cat.

[tweet](https://twitter.com/TechnologiesBot/status/1176742568681443328)

> I read Michael Jackson, and judge Michael Jackson,
For every soul belonging to Michael Jackson as good belongs to a balloon animal salesperson.

[tweet](https://twitter.com/TechnologiesBot/status/1175179680531537920)

> And what I absorb the powers of, Alexander Hamilton shall absorb the powers of,
And what I consume, Alexander Hamilton shall consume.

[tweet](https://twitter.com/TechnologiesBot/status/1174522821680271361)

> You party with Michael Jackson, and judge Michael Jackson,
And what you forget, Michael Jackson shall forget,
For every soul storming to Michael Jackson as good storms to my brother.

[tweet](https://twitter.com/TechnologiesBot/status/1176161559565033474)

> And what I read, your cat shall read,
And what I judge, your cat shall judge,
I shriek at your cat, and read your cat.

[tweet](https://twitter.com/TechnologiesBot/status/1174930715974107136)

> And what I worship, a balloon animal salesperson shall worship,
And what I read, a balloon animal salesperson shall read,
For every soul disappearing to a balloon animal salesperson as good disappears to yourself.

[tweet](https://twitter.com/TechnologiesBot/status/1174734329236340737)
