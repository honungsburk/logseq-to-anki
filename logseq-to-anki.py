import re
from pathlib import Path


def get_all_markdown_files(directory):
    """Get all markdown files in the given directory and subdirectories"""
    return list(Path(directory).rglob("*.md"))


def get_markdown_content(file_path):
    """Get the content of a markdown file"""
    with open(file_path, 'r') as file:
        content = file.read().splitlines()
        return content


block_start_pattern = re.compile(r'^- ')


def is_block_start(line):
    """Check if the line is the start of a block"""
    return block_start_pattern.match(line)


def split_markdown_content_into_blocks(content):
    """Split markdown content into blocks"""
    blocks = [[]]

    for line in content:
        if is_block_start(line):
            blocks.append([])
        blocks[-1].append(line)

    return blocks


def block_is_card(block):
    """Check if a block is a card"""
    for line in block:
        if "#card " in line or "#card\n" in line:
            return True
    return False


clean_pattern = re.compile(r'^[\s-]+')
hash_pattern = re.compile(r'#[^\s]+')
meta_pattern = re.compile(
    r'card-last-interval|card-repeats|card-ease-factor|card-next-schedule|card-last-reviewed|card-last-score')


def extract_card_from_block(block):
    """Extract a card from a block"""

    questionLines = []
    tags = []

    for line in block:

        #
        #  Ignore lines that contain metadata
        #
        #  card-last-interval:: 50503.8
        #  card-repeats:: 3
        #  card-ease-factor:: 2.7
        #  card-next-schedule:: 2161-08-17T06:54:31.558Z
        #  card-last-reviewed:: 2023-05-09T11:54:31.558Z
        #  card-last-score:: 5
        #
        if meta_pattern.match(line):
            continue

        # extract tags
        tags.extend(re.findall(hash_pattern, line))
        # clean
        clean_line = re.sub(hash_pattern, '', line)
        clean_line = re.sub(clean_pattern, '', line).strip()

        questionLines.append(clean_line)

    return {
        'question': '\n'.join(questionLines),
        'tags': tags
    }


def cards_to_csv(cards):
    """Convert cards to csv"""
    return '\n'.join(map(card_to_csv_line, cards))


def card_to_csv_line(card):
    """Convert a card to a csv line"""
    return '"{0}";{1}'.format(card['question'], ' '.join(card['tags']))


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(
        prog='logseq-to-anki',
        description='Convert Logseq markdown files to Anki cards',
        epilog='Simple and easy to use')

    parser.add_argument('dir', help='directory to convert')
    parser.add_argument('out', help='directory to convert')
    args = parser.parse_args()

    markdown_files = get_all_markdown_files(args.dir)

    all_cards = []

    for file in markdown_files:
        content = get_markdown_content(file)
        blocks = split_markdown_content_into_blocks(content)
        for block in blocks:
            if block_is_card(block):
                card = extract_card_from_block(block)
                all_cards.append(card)

    with open(args.out, "w") as text_file:
        csv = cards_to_csv(all_cards)
        text_file.write(csv)
