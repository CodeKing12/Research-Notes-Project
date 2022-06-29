---
title: "Introduction to Economics -- Lecture 2"
status: "In Progress"
tags:
    - economics
    - "demand and supply"
---

\toc

# Lecture 1

This is some random text that should show up under the heading. I am going to format text in standard ways to see how it renders. For example, this should be **bold**, this should be *italics*, this should be `code`. 

I am going to reference citation keys located in `papers/citations.bib`. The last paper I read was @berryAutomobilePricesMarket1995. I liked a, b, and c about it. I need to take notes on this paper in one of the files in the papers directory. Next, I will read @cavalloTariffPassThroughBorder2021.

## Quoted Text

Here is a quote block:

> This text is quoted.
> And this text is also quoted

## Code Blocks

Here's a python code block

```python
import pandas as pd
import numpy as np

df = pd.read_csv("data.csv")
print(df.columns)
```

Here's a Julia code block

```julia
using CSV, DataFrames, DataFramesMeta

df = CSV.read("data.csv", DataFrame)
println(names(df))
```

## Tables

| Syntax    | Description |
| --------- | ----------- |
| Header    | Title       |
| Paragraph | Text        |

## Footnotes

Here's a simple footnote,[^1] and here's a longer one.[^bignote]

[^1]: This is the first footnote.

[^bignote]: Here's one with multiple paragraphs and code.

    Indent paragraphs to include them in the footnote.

    `{ my code }`

    Add as many paragraphs as you like.

## Task Lists

- [x] Write the press release
- [ ] Update the website
- [ ] Contact the media