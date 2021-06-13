import argparse
import requests


parser = argparse.ArgumentParser()
parser.add_argument("--readwise_token",
	help="Readwise API access token (in the form \"Token XXX\")")
parser.add_argument("--print_books", dest='print_books', action='store_true',
	help="Print the book Ids and titles to the console")


def main():
	args = parser.parse_args()

	books_data = get_books_data(args.readwise_token)
	book_ids_and_titles = extract_book_ids_and_titles(books_data)

	if args.print_books:
		for book_id, book_title in book_ids_and_titles:
			print("id: {}, title: {}".format(book_id, book_title))


def get_books_data(readwise_token):
	query_string = {
		"category": "books",
	}

	return send_readwise_request("books/", readwise_token, query_string)


def extract_book_ids_and_titles(books_data):
	return [(b["id"], b["title"]) for b in books_data["results"]]


def get_highlights(readwise_token, book_id):
	query_string = {
		"page_size": 3,
		"book_id": book_id,
	}

	return send_readwise_request("highlights/", readwise_token, query_string)


def send_readwise_request(path_suffix, readwise_token, params):
	response = requests.get(
		url="https://readwise.io/api/v2/{}".format(path_suffix),
		headers={"Authorization": readwise_token},
		params=params
	)
	return response.json()


if __name__ == "__main__":
	main()
