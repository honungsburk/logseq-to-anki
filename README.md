# logseq-to-anki

A small CLI tool to convert [Logseq](https://logseq.com/) cards to [Anki](https://apps.ankiweb.net/) flashcards.

It is very simple and I've made assumptions based on how my Logseq notes are structured. It may not work for you.
Luckily, it's easy to modify the code to suit your needs.

## How it works

I went with the simplest solution which is to read through the Logseq notes and extract the information I need.
Then create a CSV file that can be imported into Anki. It looks like this:

```csv
{{c1::cloze one}} some text {{c2::cloze two}} some other text?;tag1 tag2
{{c1::cloze one}} some text {{c2::cloze two}} some other text?;tag1 tag2
...
```

you then map the first column to the first field in a cloze card and the second column to the tags field.

The output is far from perfect. I still had to do a fair bit of manual work to get the cards into a state where I could use them.
But it's a lot better than doing it all manually.

```bash
$ python3 logseq-to-anki.py PATH_TO_LOGSEQ_DATABASE OUTPUT_FILE
```
