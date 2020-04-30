# Course Graph Generator
Trying to scrape course and teacher information into one database, and then generate nice looking graphs from them. 


## Pipeline
```
[Scrape From Pitt] -> [Combine Terms] -> [Parse Prequisite Trees] -> [Convert to Graph]
```

There are a lot of edge cases. For example, in Spring 2020, the Film Studies classes had the code `FILMST`. Then, In Fall 2020, they changed to use `FMST`. Some classes are only offered in the fall, some in the spring, etc. And on the website, the prequisite strings are always so inconsitent, so it is hard to build a parser for them. 

## Visualization
After scraping the appropiate course data, the `dagre-d3` library is used to actually display these as SVGs.