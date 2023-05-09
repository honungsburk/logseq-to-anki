# logseq-to-anki

A small CLI tool to convert [Logseq](https://logseq.com/) cards to [Anki](https://apps.ankiweb.net/) flashcards.

It is very simple and I've made assumptions based on how my Logseq notes are structured. It may not work for you.
Luckily, it's easy to modify the code to suit your needs.

## How it works

I went with the simplest solution which is to read through the Logseq notes and extract the information I need.
Then create a CSV file that can be imported into Anki.
