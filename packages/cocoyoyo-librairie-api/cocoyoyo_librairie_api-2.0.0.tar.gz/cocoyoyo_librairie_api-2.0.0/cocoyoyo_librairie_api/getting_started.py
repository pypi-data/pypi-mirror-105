from pprint import pprint
from cocoyoyo_librairie_api.api import CocoyoyoLibrairie, CocoyoyoLibrairie_Exception, Decorators

""" If you want to disable the message on init: """
# module = CocoyoyoLibrairie(False)
""" else: """
module = CocoyoyoLibrairie()

# search a book
search = module.search('Petit')
""" Uncomment below to view result """
# pprint(search)

# search a book by his id
search_id = module.search_id(search['resultat_livres'][0]['id'])
""" Uncomment below to view result """
# pprint(search_id)

# search a book by his isbn (WARNING !!! ALL BOOKS FIND WITH THIS METHOD AREN'T NECESSARILY IN THE COCOYOYOLIBRAIRIE)
search_isbn = module.search_isbn(9791035204396)
""" Uncomment below to view result """
# pprint(search_isbn)

# search an user
search_user = module.search_user('No Token')
""" Uncomment below to view result """
# pprint(search_user)

# get book link by his id
book_link = module.get_book_link('book_id')
""" Uncomment below to view result """
# print(book_link)

# get book by his link
get_book_by_his_link = module.get_book_by_link('https://cocoyoyo-librairie.camponovo.space/book/6082d0cb6da28284066a9549')
""" Uncomment below to view result """
# print(get_book_by_his_link)

"""
I want to have doc of library
Uncomment below to view result
"""
# print(module.__doc__)

"""
I want to have doc of search() method
Uncomment below to view result
"""
# print(module.search.__doc__)


""" You can catch exceptions of API: """
try:
    search_user = module.search_user('00')
except CocoyoyoLibrairie_Exception as e:
    """
    instructions after catching error
    """
    # print(f'An exception occurred !\n{e.__class__.__name__}: {"".join(e.args)} !')

# advanced api functions | these functions needed to be connect:

# setup account
""" Uncomment below to view result """
# get_account = module.setup('user_name',
#                            'token',
#                            'api_key')
# all of these informations are here : https://cocoyoyo-librairie.camponovo.space/infos
# print(get_account)

# add a book
# IMPORTANT ! ALWAYS PUT VALUE AND KEYS IN DOUBLE QUOTES
""" Uncomment below to view result """
# add_book = module.add_book({"titre": "titre", "auteur": "auteur", "date": "date", "resume": "resume", "pages": "pages", "tags": "tags"})
# print(add_book)

# modify a book
# IMPORTANT ! ALWAYS PUT VALUE AND KEYS IN DOUBLE QUOTES
""" Uncomment below to view result """
# modify_book = module.modify_book('book_id', {"titre": "modifications", "auteur": "modifications", "date": "modifications", "resume": "modifications", "pages": "modifications", "tags": "modifications"})
# print(modify_book)

# delete a book
# IMPORTANT ! ALWAYS PUT VALUE AND KEYS IN DOUBLE QUOTES
""" Uncomment below to view result """
# delete_book = module.delete_book('book_id')
# print(delete_book)

""" You can use all functions above with a decorator like this: """
# IMPORTANT ! THESE FUNCTION NEED TO HAVE EXACTLY THE SAME ARGUMENTS THAN THE EXAMPLES

cocoyoyoLibrairie = Decorators(False)


@cocoyoyoLibrairie.search_user
def search_user(token, user_infos: dict):
    """ Uncomment below to view result """
    # print(f"Searching user with token {token}")
    # print(f'I found this user:\n')
    # pprint(user_infos)


""" Uncomment below to view result """
# put a valid user token token here
# search_user('token')


@cocoyoyoLibrairie.search_isbn
def search_isbn(isbn, book_infos: dict):
    """ Uncomment below to view result """
    # print(f"Searching book with isbn {isbn}")
    # print(f'I found this book:\n')
    # pprint(book_infos)


""" Uncomment below to view result """
# search_isbn(9791035204396)


@cocoyoyoLibrairie.search_id
def search_id(_id, book_infos: dict):
    """ Uncomment below to view result """
    # print(f"Searching book with isbn {_id}")
    # print(f'I found this book:\n')
    # pprint(book_infos)


""" Uncomment below to view result """
# search_id('6082d0cb6da28284066a9549')


@cocoyoyoLibrairie.search
def search(something, only_title, book_infos: dict):
    """ Uncomment below to view result """
    # print(f"Searching book {something} with parameter only_title on {only_title}")
    # print(f'I found this book:\n')
    # pprint(book_infos)


""" Uncomment below to view result """
# IMPORTANT ! ALWAYS PUT :param book_infos AT {} AND :param only_title AT False OR True
# search('Petit', False, {})


@cocoyoyoLibrairie.get_book_link
def get_book_link(_id, link):
    """ Uncomment below to view result """
    # print(f"Getting link of book_id {_id}")
    # print(f'I found this url:\n{link}')


""" Uncomment below to view result """
# get_book_link('book_id')


@cocoyoyoLibrairie.get_book_by_link
def get_book_by_link(link, infos):
    """ Uncomment below to view result """
    # print(f"Getting book {link}")
    # print(f'I found this book:\n')
    # pprint(infos)


""" Uncomment below to view result """
# get_book_by_link('https://cocoyoyo-librairie.camponovo.space/book/6082d0cb6da28284066a9549')
