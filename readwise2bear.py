"""Export highlights from Readwise to Bear."""
import argparse
import datetime
import logging
import webbrowser
import requests


logging.basicConfig(
	level=logging.INFO,
	format="%(asctime)s [%(levelname)s]: %(message)s")


parser = argparse.ArgumentParser()
parser.add_argument("--readwise_token",
	help="Readwise API access token (in the form \"Token XXX\")")
parser.add_argument("--book_id",
	help="Id of book to import and export hihglights")
parser.add_argument("--from_date", dest='from_date',
	type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
	help="Date after which (inclusive) to filter highlights")
parser.add_argument("--print_books", dest="print_books", action="store_true",
	help="Print the book Ids and titles to the console")
parser.add_argument("--dry_run", dest="dry_run", action="store_true",
	help="Dry run script (No export to Bear)")


HIGHLIGHTS_PER_PAGE = 25
HIGHLIGHT_PREVIEW_TEXT_LENGTH = 25


def main():
	args = parser.parse_args()

	logging.info("Importing books data...")
	books_data = import_books_data(args.readwise_token)
	book_ids_and_titles = extract_book_ids_and_titles(books_data)

	for book_id, book_title in book_ids_and_titles.items():
		if args.print_books:
			print("id: {}, title: {}".format(book_id, book_title))
			continue

		if args.book_id and args.book_id != book_id:
			continue

		logging.info("Importing highlights for %s (id: %s)..." % (book_title, book_id))
		highlights = import_highlights(args.readwise_token, args.book_id)
		for highlight in highlights:
			highlight_date = get_highlight_date(highlight)
			if args.from_date and highlight_date < args.from_date:
				continue

			logging.info("Exporting highlight %s" % get_highlight_preview(highlight))
			formatted_highlight = format_highlight(highlight, book_title)
			if not args.dry_run:
				export_to_bear(formatted_highlight)


def import_books_data(readwise_token):
	query_string = {
		"category": "books",
	}

	return send_readwise_request("books/", readwise_token, query_string)


def extract_book_ids_and_titles(books_data):
	return {str(b["id"]): b["title"] for b in books_data["results"]}


def import_highlights(readwise_token, book_id):
	highlights = []

	has_more_highlights = True
	page = 1
	while has_more_highlights:
		query_string = {
			"page_size": HIGHLIGHTS_PER_PAGE,
			"book_id": book_id,
			"page": page
		}

		response = send_readwise_request("highlights/", readwise_token,
			query_string)

		if "results" in response:
			highlights.extend(response["results"])
			page += 1
		else:
			has_more_highlights = False

	return highlights


def send_readwise_request(path_suffix, readwise_token, params):
	response = requests.get(
		url="https://readwise.io/api/v2/{}".format(path_suffix),
		headers={"Authorization": readwise_token},
		params=params
	)
	return response.json()


def get_highlight_date(highlight):
	assert "highlighted_at" in highlight
	return datetime.datetime.strptime(highlight["highlighted_at"], "%Y-%m-%dT%H:%M:%SZ")


def get_highlight_preview(highlight):
	assert "text" in highlight
	if len(highlight["text"]) < HIGHLIGHT_PREVIEW_TEXT_LENGTH:
		return "\"{}...\"".format(highlight["text"])
	return "\"{}...\"".format(highlight["text"][:HIGHLIGHT_PREVIEW_TEXT_LENGTH])


def format_highlight(highlight, book_title):
	assert "id" in highlight
	assert "text" in highlight
	assert "note" in highlight
	assert "location" in highlight
	assert "highlighted_at" in highlight

	formatted_highlight_lines = []
	formatted_highlight_lines.append("> {}\n".format(highlight["text"]))
	if highlight["note"]:
		formatted_highlight_lines.append("Note: {}\n".format(highlight["note"]))
	formatted_highlight_lines.append("Source: {}".format(book_title))
	formatted_highlight_lines.append("Location: {}".format(highlight["location"]))
	formatted_highlight_lines.append("Highlight date: {}".format(highlight["highlighted_at"]))
	formatted_highlight_lines.append("Readwise Id: {}\n".format(highlight["id"]))
	formatted_highlight_lines.append("[Highlight imported from Readwise and exported to Bear]")

	return "\n".join(formatted_highlight_lines)


def export_to_bear(text):
	webbrowser.open("bear://x-callback-url/create?text=%s" % text)


if __name__ == "__main__":
	main()
