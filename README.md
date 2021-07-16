# Readwise2Bear
Export your Readwise highlights to Bear.

## Requirements

Python dependencies listed in `requirements.txt`, and can be installed with,

```
pip install -r requirements.txt
```

## Usage

Find the book Id for the book highlights you want to export to Bear,

```
python3 readwise2bear.py --readwise_token "${READWISE_TOKEN}" --print_books
2021-07-15 21:54:12,191 [INFO]: Importing books data...
id: 9865221, title: Mastering Blockchain
id: 8872616, title: Ready Player Two
...
```

Then export the highlights for a book to Bear, one highlight per Bear note,

```
python3 readwise2bear.py --readwise_token "${READWISE_TOKEN}" --book_id 8872616
```

If you want to preview the exported highlights before actually exporting them,
you can use the `--dry-run` flag,


```
python3 readwise2bear.py --readwise_token "${READWISE_TOKEN}" --book_id 8872616 --dry-run
```