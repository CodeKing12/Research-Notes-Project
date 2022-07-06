# Overview

I want a python-based solution (flask or django) for organizing my personal markdown notes on the web. The notes will be stored in a private GitHub repository, while the website will be hosted elsewhere. A simple static site would not be enough since I need some features (e.g. restricted access) which are not supported by static sites.

My expected workflow is as follows: I will push markdown notes to a private github repo and the associated website will rebuild every time there's a commit to the repo. I should be able to go to the website address, put in a simple passcode, and then freely browse all my notes rendered as webpages.

The folder "papers" is special. Its contents will be handled slightly different from every other subdirectory (currently shown as "books" and "classes" but can be anything). The papers subdirectory will be used to store notes on research papers. It will also contain a .bib file which will need to be parsed using Python to render contents as per the details below. Pay special attention to differences in details for notes under "papers" and details for all other notes. 

Below is a "wishlist" of features. If you think any of them are very hard to do (or can be modified so as to make them easier to implement), reach out to me. I am happy to discuss changes. Also messgae me if you also have improvements in mind (e.g. maybe I am proposing a stupid way of doing things, and you know of a better way), This website is for personal use so my budget is not very high -- at most USD 150 (lower if possible), so feel free to propose modifications to the wishlist to bring down the total costs.

-------------------

# Main Features

## 1. Parse all markdown content

This includes all headers, text, lists, quotes, images, tables, code blocks, math (in-line and block), and links (to external website as well as my own notes using relative paths from root directory). A useful reference for parsing math could be http://rreece.github.io/sw/markdown-memo/05-math.html. (optional feature: ability to reference equations as in the linked document i.e. using `[@eq:stokes]`).

In addition, I would like to parse in-text bibliographic references corresponding to entries in the `citations.bib` file in the papers directory. An example of this (using Julia instead of Python but I am sure Pythonic solutions exist) can be found here:
- raw file: https://git.sr.ht/~adigitoleo/adigitoleo.srht.site/tree/main/item/blog/geophys/drex-tests-analytical.md
- output: https://adigitoleo.srht.site/blog/geophys/drex-tests-analytical#Kaminski2002

In the above example, citations keys are given using a function in curly brackets. I would instead like to use either `\ref{citation-key}` or use `@citation-key` in the raw markdown, which should then be expanded appropriately in-text and added under "References" at the bottom of the rendered page. For example, `@berryAutomobilePricesMarket1995` should expand to `Berry, Levinsohn, and Pakes (1995)` in the text itself, and at the bottom, a bibliographic entry should be added under "References". The bibliiographic entry could be in any popular citation style e.g. APA: 

> Berry, S., Levinsohn, J., & Pakes, A. (1995). Automobile Prices in Market Equilibrium. Econometrica, 63(4), 841–890. https://doi.org/10.2307/2171802

If more than three authors are listed, in-text reference should use the convention of "et al.". For example, `@cavalloTariffPassThroughBorder2021` should be shown as `Cavallo et al. (2021)`. These bibliographic references might be present even in notes other than the "papers" directory; these will need to be parsed and then included in a "References" section at the bottom of the rendered HTML page.

Some useful tools might be `citation.js`, `citeproc-py`, or `mdx_bib`. The latter two are python libraries.

## 2. Parse all metadata

Each file will contain a YAML header. The keys will differ depending on whether the note is under "papers" or anywhere else. See the sample markdown files to see what these headers would look like.

Under "papers", the header includes [title, year, status, tags, bibtex_ref, link]. `status` will take values such as "in progress", "up next", "completed", "on hold". These will be used later to sort the notes in an index page. `tags` are self-explanatory.

The most non-obvious entry is `bibtex_ref`. It is the the key in the .bib file which uniquely identifies the research paper that is being studied/summarized in the markdown file. For example, 

```yaml
bibtex_ref: berryAutomobilePricesMarket1995
```

We will use this YAML key to get relevant metadata such as title of the research paper, names of authors, year, journal etc. As discussed below, we will use these metadata to create an index file for the "papers" directory. We will also generate a bibliographic reference for the paper and show it below the paper title in the rendered html page for this markdown file.

Finally, `link` is a link to the pdf of the research paper, saved on dropbox. We will use this to create a link so I can easily navigate to the underlying pdf from the webpage containing notes about this pdf.
     
Under all other directories, YAML header would only include [title, status, tags].

## 3. Navigation

Webpage addresses should be constructed using nested structure of the directories and the YAML "title" of the markdown file. These should be in kebab case e.g. `xxxx.com/classes/econ101/my-first-note.md`

## 4. Indexing

Each time the site is built, an index page should be automatically generated for each subdirectory. This index/landing page would contain links to all other files in the same subdirectory. The links should use the YAML title as the displayed text or in the case of files under "papers", the title from the relevant `bibtex_ref` entry (if available)

The index page should allow one to sort results by `created_on` and `modified_on`. These are datetime properties and should be grabbed from the file metadata. One should also be able to sort them by `status` + `title`, where status would include manually fed entries such as "in progress", "up next", "completed", "on hold". It would be nice if the results sorted by `status` were grouped into subsections, with each subsection heading being the appropriate category such as "completed". I will call this feature "groupby-sort".

The index page for "papers" should show year and journal (from `bibtex_ref` if available) or just year (from metadata) next to each paper title. Below the paper title, in small font, authors for each paper must be displayed (if available from `bibtex_ref`). 

The index page for all other subdirectories should display just the titles with options to sort by `title`, `created_on`, `modified_on`, or groupby `status` and then sort by `title`.


## 5. Search

Website should be searchable (like this: https://just-the-docs.github.io/just-the-docs/). It should also be searchable by tags (even if they are not rendered in the html). One easy solution would be to have a page dedicated to tags where all the tags are listed sorted by how often they were used. When search results are shown, they should be sorted by directories/subdirectories, and/or bread crumbs navigation to each search result should be shown. 

## 6. Restricted Access

I do not want my private notes to be freely available on the internet; nor do I want the security to be bulletproof. Just a simple deterrent such as a 6-digit passcode would be enough. This should only be required once when visitng the website; on subsequent webpages, no passcode should be required.


-------------------

# Aesthetic Features

Here's a rough sketch of the layout for notes. 

```
┌────────┬──────────────────────┬─────┐
│        │ PAPER TITLE          │     │
│        │                      │     │
│        ├──────────────────────┤     │
│        │# H1                  │     │
│MAIN    │                      │     │
│NAV     │<TEXT>                │     │
│        │                      │ TABLE
│        │                      │ OF  ┼
│        │                      │ CONTENTS
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
│        │                      │     │
└────────┴──────────────────────┴─────┘
```

The main navigation should be automatically generated. The navigation bar would be nested based on directory structure e.g. notes saved under classes > econ101 should show up under the appropriate navigation item on the left. For inspiration, see the navigation bar here: https://just-the-docs.github.io/just-the-docs/docs/ui-components/code/line-numbers/

Note that this should adapt accordingly for mobile (just as it does in the example website).

On each page, breadcrumbs navigation should be present at the very top (above the title) just like here: https://just-the-docs.github.io/just-the-docs/docs/ui-components/code/line-numbers/
(side note: I like how the links are styled here so you can use this for design inspiration too).

Finally, using a `\toc` or `\tableofcontents` command in the raw markdown document shoul generate an in-document navigation on the right side of the screen (like this: https://tlienart.github.io/Xranklin.jl/syntax/extensions/). This should stay fixed as one scrolls up and down on the main content.


Other details:
- For papers, use the `bibtex_ref` to get metadata such as paper title, authors, year, and journal. If these are not available (i.e. `bibtex_ref` is blank or parser gives blanks), just use title and year from the YAML header. Place the paper title under bread crumbs (in large font size), authors in the next line (small, gray), and year and journal on the line after that (small and gray). Finally, use a block to show the full bibliographic reference (APA style) right before the main text starts i.e. above # H1 in the layout above.
- For other notes, just show the note title specified in the YAML header. 
- The left column needs to be similar to `just-the-docs` while the right column (narrower than the left column) should look like https://tlienart.github.io/Xranklin.jl/syntax/extensions/



-------------------

# Bonus:

- I value aesthetics a lot. You have artistic freedom but something clean, modern, and not distracting would be great (similar to `just-the-docs` theme). If you use a primary color for the website, define it at the beginning of the css/scss file so I can play with it in case I want a different primary/secondary color.
- Dark mode
