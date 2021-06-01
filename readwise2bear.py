import argparse
import requests

parser = argparse.ArgumentParser()
parser.add_argument("--readwise_token", help="Readwise API access token (in the form \"Token XXX\")")

def main():
	args = parser.parse_args()

	books_data = get_books_data(args.readwise_token)
	book_ids_and_titles = extract_book_ids_and_titles(books_data)

	for b in book_ids_and_titles:
		print("id: %s, title: %s" % b)

def get_books_data(readwise_token):
	querystring = {
	    "category": "books",
	}

	response = requests.get(
	    url="https://readwise.io/api/v2/books/",
	    headers={"Authorization": readwise_token},
	    params=querystring
	)

	return response.json()

def extract_book_ids_and_titles(books_data):
	return [(b["id"], b["title"]) for b in books_data["results"]]

if __name__ == "__main__":
	main()
