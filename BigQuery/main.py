import requests

r = requests.get('https://pokeapi.co/api/v2/pokemon')

# r.status_code

# r.headers['content-type']

# r.encoding

# print(type(r.text))

pokelist = []
pokedict = {}


# result["name"] = "bulba"
# result["type"] = "grass"


r_js = r.json()

def add_to_dict(dict_name, key, value):
	dict_name[key] = value

i = 0
for var in r_js.get("results"):

	# key = next(iter(var))
	# value = 

	pokedict["name"] = var["name"]
	print(pokedict)
	pokelist.append(pokedict)

	url = var.get("url")
	r = requests.get(url)
	# print ( r.json().get("types")[0].get("type").get("name") )

	i += 1
	if (i == 3):
		break	

