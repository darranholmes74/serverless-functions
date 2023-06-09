from http.server import BaseHTTPRequestHandler
from urllib import parse
import requests


class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        s = self.path
        url_components = parse.urlsplit(s)
        query_string_list = parse.parse_qsl(url_components.query)
        dic = dict(query_string_list)

        if "country" in dic:
            url = f"https://restcountries.com/v3.1/name/{dic['country']}?fullText=true"
            r = requests.get(url)
            data = r.json()
            countries = []
            for word_data in data:
                country = word_data["capital"][0]
                countries.append(country)
            message = f"The capital of {dic['country']} is {', '.join(countries)}"
        elif "capital" in dic:
            url = f"https://restcountries.com/v3.1/capital/{dic['capital']}?fullText=true"
            r = requests.get(url)
            data = r.json()
            countries = []
            for word_data in data:
                country = word_data["name"]["common"]
                countries.append(country)
            message = f"{dic['capital']} is the capital of {', '.join(countries)}"
        else:
            message = "Give me a country name please"

        self.send_response(200)
        self.send_header('content-type', 'text/plain')
        self.end_headers()

        self.wfile.write(message.encode())

        return

