# Lab Report: Corpus Analysis

#### Jack Nolan

## Process Description

This lab report was basically an extension of Lab 9, which was about Text as Data generally. This lab, instead of merely exploring a single source of text, we looked at combining the data of multiple sources (science fiction novels in our case) and deriving some information about some large swath of texts.

In order to do this, we used the R programming language again on NEU's [R studio server](http://rstudio.library.northeastern.edu/). This time, we went through the file `lab10-CorpusAnalysis.Rmd`, discussing each block of code and how it works and what it is doing.

Specifically, we looked at a collection of Science Fiction novels from Project Guttenberg. Ideally, we would have looked at the entire Sci-Fi bookshelf on Project Guttenberg but that probably would have killed our server, so we only looked at a collection of 150 novels collected conveniently in a CSV file.

Then, we used a process called sentiment analysis on the corpus, at first in order to see which books were the "angriest" and later which novels were the fairest or "trusting". This was accomplished by counting the number of words in the book that would fit into some sentiment, and then dividing this number by the length of the book.

For the angriest books, this gave us this list:
![list of the angriest sci-fi novels](/images/angriestBooks.png)

For the fairest / most trusting books, I got this list:
![list of the fairest / most trusting sci-fi novels](/images/fairestBooks.png)

Then, we used topic modelling to explore the nine titles which seemed the angriest. This was done by first chunking the text into 100 word chunks. Using "beta" measurement, we could explore which words belonged to which subjects in the chunks, and using "gamma" measurement, we could explore what the topics of the entire text are, and how the topics of the text change across the book.

## Observations

Although I am CS major, I don't have much experience using R, so I'm always excited to learn about some new programming language. I missed the lab report about the first part of this lab, so I will include a couple of my observations here in this lab report. First of all, I actually really like the way variables get set, using the arrow `<-` because it is very explicit as to what is happening. You won't get it confused with comparisons `==`. I also find the extensive use of pipes `%>%` to be really interesting. I am used to using pipes in the terminal (stylized as `|`), but generally when passing outputs of one function to the inputs of the next, I am much more used to just layering the different functions inside of one another. And while this might seem simpler to me because I am used to looking at inputs and outputs in this way, I can see why using the pipes could be generally easier to understand.

Obviously, R is a programming language designed for statistical analysis and plotting graphs and that kind of dealing with large data sets, but I am really impressed at how the production of graphs was so integrated into the language. Also, the language seems well put together for general research. I have heard that a lot of scientists don't release the code that they wrote in order to parse some data because they are "ashamed" of it because it is sloppy or hacked together. It feels like if you are writing statistical code, it would be much harder to write sloppy, totally incomprehensible code in R than in a more general-purpose language like Python or Java.

## Analysis

My first Unessay project, my poetry generator, acted kind of like an inverse to this lab. Especially because of my use of the [datamuse API](https://www.datamuse.com/api/). For that API, they had collected all of this kind of data to build a huge set of parameters on how different words were correlated. Sure, finding words which are synonyms and antonyms is relatively simple if you just parse a database which has just been pre-assembled by humans, determining if different words are just generally related in much more difficult. This kind of analysis falls much more into the "Beta" form of analysis. I would imagine datamuse collected their textual data from a very wide arrange of sources because you can give it just about any word or phrase and it can give you a whole bunch of related words and phrases, often related in ways that seem obvious, but at other times related in other entirely unexpected ways. Datamuse also pulls data from other sources, like Google's Ngrams, which it mainly uses to tell you a list of words that generally directly follows or proceeds some other word, and give you lists of adjectives that relate to some noun, or nouns that relate to some adjective. However, Ngram analysis is something that we mainly went over in the first coding lab, except that Google has managed to run this analysis on millions of books, making their dataset pretty incredible.

However, one should keep in mind the source of the data that all of this is coming from. Using datamuse, the occasional swear word or offensive phrase will slip through all of its filters because of its data sources. This is a stark reminder that the source of your data matters. As Catherine D'Ignazio and Lauren Klein remind us, in "What gets Counted Counts," your data source matters, especially when your data source is people. Humans are weird and wacky and hard to categorize. Just having a name like "Null" could really mess up websites. I think a lot of the problems here come down to bad planning for the future. We live in a world where moving from an old database to a new database or changing other code-architecture changes could take months and cost millions of dollars, meaning such a change must make financial sense to do for the company. 

The problem with a lot of websites, like Facebook, is that they were initially hacked together in a very short amount of time, with no expectation that it would one day become such a global superpower that it is today. This is like those scientists who do not want to share their code because they are "ashamed" of it, the core of Facebook's technology relied on how Mark Zuckerberg saw the world. Clearly, he was misguided in his beliefs (Wikipedia states that Facebook had initially started as a "Hot or Not" website) and didn't account that people would initially identify as more than the binary "male" or "female." As is mentioned in the article, a lot of software engineers report themselves as male, which is a huge problem and can often lead to these kinds of mistakes. This is a huge part of the initiative for organizations like *Girls Who Code* and other organizations trying to get a wider diversity of people interested in coding. A wider diversity of people making the products **will** result in better, more widely usable products. Because, people design things for themselves, so having lots of very different people on a team making a product will result in a better experience for more people, generally. This is another major reason while Ada Lovelace is getting upheld as the mother of computer science - in order to try to inspire more people, who do not identify as "men," to join the field.



----

Note: Sorry this is late by a bit. By my course contract this should still be ok.

