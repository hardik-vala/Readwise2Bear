import argparse
import datetime
import json
import requests
import webbrowser


parser = argparse.ArgumentParser()
parser.add_argument("--readwise_token",
	help="Readwise API access token (in the form \"Token XXX\")")
parser.add_argument("--from_date", dest='from_date',
	type=lambda s: datetime.datetime.strptime(s, "%Y-%m-%d"),
	help="Date after which (inclusive) to filter highlights")
parser.add_argument("--print_books", dest='print_books', action='store_true',
	help="Print the book Ids and titles to the console")


def main():
	args = parser.parse_args()

	books_data = get_books_data(args.readwise_token)
	book_ids_and_titles = extract_book_ids_and_titles(books_data)

	for book_id, book_title in book_ids_and_titles:
		if args.print_books:
			print("id: {}, title: {}".format(book_id, book_title))
		else:
			highlights = get_highlights(args.readwise_token, book_id)
			for highlight in highlights:
				highlight_date = datetime.datetime.strptime(highlight["highlighted_at"], "%Y-%m-%dT%H:%M:%SZ")
				if highlight_date >= args.from_date:
					webbrowser.open("bear://x-callback-url/create?text=%s" % highlight)
					break
		break
			

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

	response = send_readwise_request("highlights/", readwise_token,
		query_string)
	
	return response["results"]


def send_readwise_request(path_suffix, readwise_token, params):
	response = requests.get(
		url="https://readwise.io/api/v2/{}".format(path_suffix),
		headers={"Authorization": readwise_token},
		params=params
	)
	return response.json()


if __name__ == "__main__":
	main()
