# Unessay Project #1:

## Poetrry Generator

#### Jack Nolan

This poetry bot was written in [Python 3](https://www.python.org/downloads/release/python-380/).
This also uses a couple of libraries which are not included in the source code. 
These can be downloaded with the following commands:

```
pip3 install urllib3
pip3 install syllables
pip3 install pronouncing
pip3 install inflect
```

Those are using pip3 because I used python 3. On my Mac, python2 is the default and comes pre-installed so its important to always specifcy the 3.

All of the other sources I used while coding have also been linked in the code.

### How to use this program

This currently only exists in the command line format, which I know is a little bit annoying. I still hope to make a discord bot out of this sometime, but that will still pretty much act just like the command line, where you send a command, and then the bot replies with a poem. The benefit of that is just that you don't need to have all the source code on your. computer to make it work.

Simple examples:

I have hardcoded in a couple of different poem types to make testing easier

In order to get a random haiku do: `./poetryGen.py haiku`

Which will output something like:
```
A human dozen
Brewer bores. Robing greases
Cracking the story.
```

In order to get a random Shakespearean sonnet do: `./poetryGen.py sonnet`
This is definetly not the best, but it does often manage to rhyme, or almost rhyme the lines as expected, and usually gets the correct number of syllables per line.

```
Stripping the barrier rolls. You wait. No!
Rings. Oh. You list it. Inviting the fat
Nightmare is to divide instead of au.
I am across the carnivorous bat.
Reducing below it or since barons
Are me. Chasing instead of the famous
Unreasonable souvenir but not before
An infamy hopes. Batting against a
Republic excites they. Ladle! I hug
Me. Concerning apparatuses are
Squeezing the Oceanic inform smug
Territorial fraudulent adar.
I level it. They are the thread. You mix
They. Redundancies give it the deep six.
```

This poetry bot can also generate poems of any form you want if you give it a correctly formated template.
This will look like a bunch of number, string pairs, seperated only by commas.

For example: a haiku looks like '5,7,5'.
The first line has 5 syllables, the second line has 7 syllables, and the third line has 5 syllables.

A rhyming couplet might look like: '5A,5B,5A,5B'.
Each line has a length of 5, and the first and third lines will try to rhyme and the second and fourth lines will try to rhyme. This will try to generate a poem like so:
```
./poetryGen.py "5A,5B,5A,5B"

Enjoying instead
Of the sidewalk or
Across the brain dead
Albacore abhor.
```

You can even do some really weird poetry formats!
```
./poetryGen.py "3A,12,3A,3A,1,2B,2B"

No! I whine
You. You bruise to blot. Vogue. They are the no-fly soft
Adeline.
I align.
Yes!
Worthless
Shawls pour
```

You can also optionally make the poem try to generate about a specific thing, using the  `--topics` flag. This should a list of comma seperated words.
For example. If I want to make a rhyming couplet about space, I would do:

```
./poetryGen.py "15A,15A" --topics="space"

I treat. It is they. Loading punishs. Span before gridlocks but
Not by the foggy hostility parking. It jut me. Glut.
```

Interestingly, the API I am using to get related words must have decided that 'space' was referring to 'parking spaces' and thus generated a poem kind of about traffic. Lets try that again but with different inputs.
```
./poetryGen.py "15A,15A" --topics="planets,unknown"

Orbs. Stars inhabited. A minor tuning neighboring me.
I am me. The american angelica tree agree.
```

There ya go, 'Stars inhabited' sounds all spacey!

### Current State of the program

For some reason, I had strongely believe that this would be much easier to create in a much shorter amount of time than it actually took! For that reason, I would say there are still quite a few improvements that couple be made. First, there could be more sentence variety in the `sentence-formats.json` file. Currently, this only generates relatively simple independent-clauses. Of course, we are already generating lots of meaningless sentences, but occasionally a beauty comes out, like 'A larceny retires behind cilantros or inside it.' It would be great if I could keep tinkering with this file to get more kinds of sentences out of it.

Another thing which would improve the quality of output is increasing the number and variety of words in the files `adjs.json`, `nouns.json`, and `verbs_with_conjugations`. I have spent some time removing words and adding words to these files to try to improve the generated poems, but really these files just need a lot more words in them.

On the actual program side. The main bug which often causes lines of the poem to end without rhyming is when they end on some grammatical word, like 'a' or 'the' which will not rhyme with the word they are supposed to rhyme against. Initially, the plan was try keep trying to regenerate the rest of the sentnce until we could find a word that rhymed. Another issue was that occasionally a word at the end of a line would have very few rhymes or near-rhymes, meaning that it would be impossible to find a rhyme later on anyway. This would be resolved by just continually retrying to choose a final word with lots of rhymes or near-rhymes so that it is more likely that we will be able to find rhymes down the road. I actually would still like to implement this sometime, but it was too complex to complete before this assignment was due. 

I think something that might improve the flow of the setences is to specifically try to get the ends of sentences or commas in the sentences to land on the ends of lines, which would probably make the poems flow better because you are more likely to stop on the correct words and this is almost certainly more likely to result in a noun or a verb at the end of the sentence which we can generally find a rhyme for.

I think part of programming literacy is that code is produced iteratively. Something which starts small can grow in complexity and ability. It's pretty rare for a program to be totally complete, with all of the functionality that you could ever hope to put into it implemented perfectly. Just like all programs, this is also a bit of a work-in-progress. Which is not to say that it doesn't work, but to say that it could be better. I tried to keep the library with all of the code, `poetryGenLib.py`, relatively organized and will commented so you can read through the code at your leisure. It is, however, still a bit of a spaghetti bowl, partially because the english language is a bit of a spaghetti bowl.

### Inspiration

The inspiration for this mostly came from our second lab where we made poetry-bots. I kept thinking about whether there was any way to try to generate more complex poems, especially something like a sonnet with its specific number of syllables per line and rhyming scheme. Then, upon finding the [DataMuse](https://www.datamuse.com/api/) I thought that it might be possible. Originally, I had started working on JavaScript, but then changed to Python because of its wealth of libraries, and because it is easy to make single-threaded calls to APIs, which makes the whole program much simpler.

After reading about [*Cent Mille Milliards*](https://en.wikipedia.org/wiki/Hundred_Thousand_Billion_Poems), I have wanted to create my own version, except this can create much more than a hundred thousand billion poems because each words can be replaced with another. Of course, a lot of these poems will not be very good, but neither would all of Raymond Queneau's original poems be either. At least with this poetry bot, each poem is much more unique, full of strange sentences which don't quite work. The resulting poems almost sound like something by Christopher Knowles, they are just such an onslaught of words which feel mostly unrelated to eachother but still find themselves in the same sentence. I actually think the poems generated by the bot actually do not sound all that bad when read aloud. Of course, even if they have the format of a sonnet, they don't end up sounding at all like a sonnet, which is interesting.

### Sources

I used a lot of sources on grammar while working on the `sentence-formats.json` file for generating different kinds of sentences.

* Extremely helpful site on quantifying different sentences and types of caluses and phrases - http://www.pitt.edu/~atteberr/comp/0150/grammar/grammarrev.html
* On prepositions - https://www.merriam-webster.com/dictionary/preposition
* On verbs - https://prowritingaid.com/Verbs
* On determiners - https://en.wikipedia.org/wiki/English_determiners
* On analyzing a sentence structure - https://www.nltk.org/book/ch08.html - I do the opposite of this to generate new (mostly) grammatically correct sentences.


I definitely felt a little bit silly look up all this English grammar which is built so far into my brain that it was hard to formalize the exact ways sentences are actually built up. 

