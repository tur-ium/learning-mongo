import pymongo
from pprint import pprint

client = pymongo.MongoClient(
    host="127.0.0.1",
    port=27017
)

print(client.list_database_names())

sample = client['sample']

# Put the zips collection from the sample database into the c_zips variable and call the find_one method:
c_zips = sample['zips']
pprint(c_zips.find_one())

random_data = [
  {"name": "Melthouse","bread":"Wheat","sauce": "Ceasar"},
  {"name": "Italian BMT", "extras": ["pickles","onions","lettuce"],"sauce":["Chipotle", "Aioli"]},
  {"name": "Steakhouse Melt","bread":"Parmesan Oregano"},
  {"name": "Germinal", "author":"Emile Zola"},
  {"pastry":"cream puff","flavour":"chocolate","size":"big"}
]

# rand = sample.create_collection(name="rand",check_exists=False)
# rand.insert_many(random_data)

# find with limit
print('An example find with a limit')
pprint([x for x in c_zips.find({},{'city':1}).limit(10)])

# find with distinct
print('Distinct states in the dataset:')
pprint([x for x in c_zips.find({},{'city':1}).distinct('state')])
print(f"That's {len(c_zips.find({},{'city':1}).distinct('state'))} US states")


# find with regex
print('Some cities in the dataset that have numbers as names: ')
import re
re_is_an_int = re.compile('^[0-9]*$')
pprint([x for x in c_zips.find({'city': re_is_an_int},{'city':1}).limit(10)])
# This is quite a nice way to find invalid data
# It is also possible to use regular expressions on the MongoDB Shell via the $regex keyword.

# Get the company that acquired Tumblr
print('The company that acquired Tumblr is ...')
pprint(
    list(
        client["sample"]["companies"].aggregate(
            [
                {"$match": {"acquisitions.company.name": "Tumblr"}},
                {"$project": {"_id": 1, "society": "$name"}}
            ]
        )
    )
)

