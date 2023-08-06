"""
Official CocoyoyoLibrairie API:
You can run the getting_started.py file to start with the api !
"""


from requests import get as g
from json import loads as j_l
import json
import requests
import colorama


__title__ = 'CocoyoyoLibrairie Official API'
__description__ = 'CocoyoyoLibrairie Official API.'
__url__ = 'https://www.camarm.dev'
__max_version__ = g('https://www.camarm.dev/api/cocoyoyo-librairie_official_api/version').content.decode("utf-8")
__version__ = "2.0.0"
__author__ = 'CAMARM-DEV'
__author_email__ = 'armand.camponovo@icloud.com'
__copyright__ = 'Copyright 2021 CAMARM-DEV, inc'


class CocoyoyoLibrairie:
    """
    Official CocoyoyoLibrairie API:
    You can run the getting_started.py file to start with the api !
    1) Import module:

    `from cocoyoyo_librairie_api.api import CocoyoyoLibrairie`

    2) Create a variable to init the api:

    `module = CocoyoyoLibrairie()`

    3) Use search methods:

    `search = module.search('Petit')
    pprint(search)

    search_id = module.__getitem__(search['resultat_livres'][0]['id'])
    pprint(search_id)

    search_isbn = module.search_isbn(9791035204396)
    pprint(search_isbn)`

    4) You can view doc on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api or simply with this code:

    `# I want to have doc of library
    print(module.__doc__)
    # I want to have doc of search() method
    print(module.search.__doc__)`

    5) You can download getting_started.py file on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api
       You can disable this message just with add `False` between init variable's parentheses:
       `module = CocoyoyoLibrairie(False)`
    """

    def __init__(self, getting_started_message=True):
        self.base_link = "https://cocoyoyo-librairie.camponovo.space/api/"
        self.book_isbn_link = self.base_link + "book-isbn:"
        self.book_id_link = self.base_link + "cocoyo-books:"
        self.book_search_link = self.base_link + "search:"
        self.book_add_link = self.base_link + "add_book/"
        self.book_modify_link = self.base_link + "modify_book/"
        self.book_delete_link = self.base_link + "del_book/"
        self.user_token_link = self.base_link + "user_token:"
        self.base_book_link = "https://cocoyoyo-librairie.camponovo.space/book/"
        self.base_book_find_one_link = self.base_link + "book_find_one/"
        self.informations = ()
        self.base_valid_link = ""
        if type(getting_started_message) is not bool:
            raise CocoyoyoLibrairie_Exception('getting_started_message must be boolean')
        if getting_started_message:
            print(CocoyoyoLibrairie.__doc__)

    def setup(self, user_name, user_token, user_api_key):
        """
        Setup your api information to add and modify books !
        :param user_name: your user_name
        :param user_token: your token
        :param user_api_key: your api key
        :return:
        """
        self.informations = (user_name, user_token, user_api_key)
        self.base_valid_link = "/" + user_name + "/" + user_token + "/" + user_api_key
        get_account = g('http://127.0.0.1:3000/api/' + 'valid_account/' + user_name + '/' + user_token + '/' + user_api_key).content.decode("utf-8")
        if get_account == "True":
            return "Correct informations"
        else:
            raise CocoyoyoLibrairie_Exception('informations are not good')

    # noinspection PyDefaultArgument
    def add_book(self, book_info: dict = {"titre": "titre", "auteur": "auteur", "date": "date", "resume": "resume", "pages": "pages", "tags": "tags"}):
        """
        Add a book
        :param book_info: info of book you want to add ({"titre": 'titre', "auteur": "auteur", "date": "date", "resume": "resume", "pages": "pages", "tags": "tags"})
        :return:
        """
        try:
            t = book_info["titre"]
            t = book_info["auteur"]
            t = book_info["date"]
            t = book_info["resume"]
            t = book_info["pages"]
            t = book_info["tags"]
        except Exception as e:
            raise CocoyoyoLibrairie_Exception("informations are not good, they must be {\"titre\": 'titre', \"auteur\": 'auteur', \"date\": 'date', \"resume\": 'resume', \"pages\": 'pages', 'tags': 'tags'}")
        result = g(self.book_add_link + str(book_info) + self.base_valid_link).content.decode("utf-8")
        if result == "added":
            return "added"
        else:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                              "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                              "Api/issues")

    # noinspection PyDefaultArgument
    def modify_book(self, _id, book_info: dict = {"titre": "titre", "auteur": "auteur", "date": "date", "resume": "resume", "pages": "pages", "tags": "tags"}):
        """
        Modify a book
        :param _id: the id of the book you want to modify
        :param book_info: infos modify ({"titre": 'titre', "auteur": "auteur", "date": "date", "resume": "resume", "pages": "pages", "tags": "tags"})
        :return:
        """
        try:
            t = book_info["titre"]
            t = book_info["auteur"]
            t = book_info["date"]
            t = book_info["resume"]
            t = book_info["pages"]
            t = book_info["tags"]
        except Exception as e:
            raise CocoyoyoLibrairie_Exception("informations are not good, they must be {\"titre\": 'titre', \"auteur\": 'auteur', \"date\": 'date', \"resume\": 'resume', \"pages\": 'pages', 'tags': 'tags'}")
        result = g(self.book_modify_link + _id + "/" + str(book_info) + self.base_valid_link).content.decode("utf-8")
        if result == "modified":
            return "modified"
        else:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                              "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                              "Api/issues")

    # noinspection PyDefaultArgument
    def delete_book(self, _id):
        """
        Modify a book
        :param _id: the id of the book you want to delete
        :return:
        """
        result = g(self.book_delete_link + _id + self.base_valid_link).content.decode("utf-8")
        if result == "deleted":
            return "deleted"
        else:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                              "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                              "Api/issues")

    def search(self, something, only_title=False):
        """
        Search a book in cocoyoyo_librairie (by date, author, title or tags)
        :param something: something to search
        :param only_title: only search by title
        :return: results of your search
        """
        if type(only_title) is not bool:
            raise CocoyoyoLibrairie_Exception('parm only_title must be boolean')
        if only_title:
            try:
                result = j_l(g(self.book_search_link + something).content)['resultat_livres']
                return result
            except Exception as e:
                raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
            except:
                raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                                  "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                                  "Api/issues")
        else:
            try:
                result = j_l(g(self.book_search_link + something).content)
                return result
            except Exception as e:
                raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
            except:
                raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                                  "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                                  "Api/issues")

    def search_id(self, book_id):
        """
        Get infos of a book by his id
        :param book_id: id of book
        :return: infos of book
        """
        if type(book_id) is not str and type(book_id) is not int:
            raise CocoyoyoLibrairie_Exception('parm book_id must be str or int')
        try:
            return j_l(g(self.book_id_link + str(book_id)).content)
        except Exception as e:
            raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
        except:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                              " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                              "es")

    def search_isbn(self, isbn):
        """
        Search a book by his isbn
        WARNING !!! ALL BOOKS FIND WITH THIS METHOD AREN'T NECESSARILY IN THE COCOYOYOLIBRAIRIE
        :param isbn: isbn of book
        :return: info of book
        """
        if type(isbn) is not str and type(isbn) is not int:
            raise CocoyoyoLibrairie_Exception('parm isbn must be str or int')
        try:
            return j_l(g(self.book_isbn_link + str(isbn)).content)
        except Exception as e:
            raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
        except:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                              " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                              "es")

    def search_user(self, token):
        """
        Get the user's informations by his token (if you put :param token: at 'No Token' you got the number of click of
         our redirections links)
        :param token: token of user
        :return: infos of user
        """
        if type(token) is not str and type(token) is not int:
            raise CocoyoyoLibrairie_Exception('parm token must be str or int')
        try:
            if token == 'No Token':
                return j_l(g(self.user_token_link + str(token)).content)['views']
            else:
                return j_l(g(self.user_token_link + str(token)).content)
        except json.decoder.JSONDecodeError:
            raise CocoyoyoLibrairie_Exception('No User Found With This Token')
        except Exception as e:
            raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
        except:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                              " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                              "es")

    def get_book_link(self, book_id):
        """
        Get the book link with the book id
        :param book_id: book id
        :return:
        """
        return self.base_book_link + book_id

    def get_book_by_link(self, link):
        """
        Get the infos of a book with his link
        :param link: link of book
        :return:
        """
        result = eval(g(self.base_book_find_one_link + link.replace('https://cocoyoyo-librairie.camponovo.space/book/', '')).content.decode("utf-8").replace("ObjectId(", "").replace("\')", "\'"))
        return result

    def credits(self):
        """
        CocoyoyoLibrairie Official API made with ❤️ by CAMARM-DEV for CAMARM-DEV, inc
        https://www.camarm.dev
        http://www.camarm.fr
        http://www.camponovo.space
        https://cocoyoyo-librairie.camponovo.space
        """
        print(self.credits.__doc__)


class Decorators:
    """
    All Cocoyoyolibrairie() methods but in decorator
    """
    def __init__(self, getting_started_message=True):
        self.base_link = "https://cocoyoyo-librairie.camponovo.space/api/"
        self.book_isbn_link = self.base_link + "book-isbn:"
        self.book_id_link = self.base_link + "cocoyo-books:"
        self.book_search_link = self.base_link + "search:"
        self.book_add_link = self.base_link + "add_book/"
        self.user_token_link = self.base_link + "user_token:"
        self.base_book_link = "https://cocoyoyo-librairie.camponovo.space/book/"
        self.base_book_find_one_link = self.base_link + "book_find_one/"
        self.informations = ()
        self.base_valid_link = ''
        if type(getting_started_message) is not bool:
            raise CocoyoyoLibrairie_Exception('getting_started_message must be boolean')
        if getting_started_message:
            print(Decorators.__doc__)

    def search(self, func):
        """
        Search a book in cocoyoyo_librairie (by date, author, title or tags) but in a decorator
        """
        def search_dec(*args):
            something = args[0]
            only_title = args[1]
            if type(only_title) is not bool:
                raise CocoyoyoLibrairie_Exception('parm only_title must be boolean')
            if only_title:
                try:
                    infos = j_l(g(self.book_search_link + something).content)['resultat_livres']
                    ret = func(something, only_title, infos)
                    return ret
                except Exception as e:
                    raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
                except:
                    raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                                      "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                                      "Api/issues")
            else:
                try:
                    infos = j_l(g(self.book_search_link + something).content)
                    ret = func(something, only_title, infos)
                    return ret
                except Exception as e:
                    raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
                except:
                    raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please re"
                                                      "port it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_"
                                                      "Api/issues")
        return search_dec

    def search_id(self, func):
        """
        Get infos of a book by his id but in decorator
        """
        def search_id_dec(*args):
            try:
                book_id = args[0]
                if type(book_id) is not str and type(book_id) is not int:
                    raise CocoyoyoLibrairie_Exception('parm book_id must be str or int')
                infos = j_l(g(self.book_id_link + str(book_id)).content)
                ret = func(book_id, infos)
                return ret
            except Exception as e:
                raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
            except:
                raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                                  " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                                  "es")
        return search_id_dec

    def search_isbn(self, func):
        """
        Search a book by his isbn but in decorator
        WARNING !!! ALL BOOKS FIND WITH THIS METHOD AREN'T NECESSARILY IN THE COCOYOYOLIBRAIRIE
        """
        def search_isbn_dec(*args):
            try:
                isbn = args[0]
                if type(isbn) is not str and type(isbn) is not int:
                    raise CocoyoyoLibrairie_Exception('parm isbn must be str or int')
                infos = j_l(g(self.book_isbn_link + str(isbn)).content)
                ret = func(isbn, infos)
                return ret
            except Exception as e:
                raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
            except:
                raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                                  " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                                  "es")
        return search_isbn_dec

    def search_user(self, func):
        """
        Get the user's informations by his token (if you put :param token: at 'No Token' you got the number of click of
         our redirections links) but in decorator
        """
        def search_user_dec(*args):

            try:
                token = args[0]
                if type(token) is not str and type(token) is not int:
                    raise CocoyoyoLibrairie_Exception('parm token must be str or int')
                infos = j_l(g(self.user_token_link + str(token)).content)
                ret = func(token, infos)
                return ret
            except json.decoder.JSONDecodeError:
                raise CocoyoyoLibrairie_Exception('No User Found With This Token')
            except Exception as e:
                raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
            except:
                raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                                  " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                                  "es")
        return search_user_dec

    def get_book_link(self, func):
        """
        Get the book link with the book id but in decorator
        """
        def get_book_link_dec(*args):
            book_id = args[0]
            link = self.base_book_link + book_id
            ret = func(book_id, link)
            return ret
        return get_book_link_dec

    def get_book_by_link(self, func):
        """
        Get the infos of a book with his link but in decorator
        """
        def get_book_by_link_dec(*args):
            link = args[0]
            infos = eval(g(self.base_book_find_one_link + link.replace('https://cocoyoyo-librairie.camponovo.space/book/', '')).content.decode("utf-8").replace("ObjectId(", "").replace("\')", "\'"))
            ret = func(link, infos)
            return ret
        return get_book_by_link_dec


class CocoyoyoLibrairie_Exception(Exception):
    """
    Exceptions of CocoyoyoLibrairie API
    """


if __name__ == '__main__':
    pass
else:
    colorama.init()
    __new_version__ = __version__.replace('.', '')
    __new_max_version__ = __max_version__.replace('.', '')
    if int(requests.__version__[:1]) < 2:
        raise CocoyoyoLibrairie_Exception(f"The version of your requests lib isn't valable, she must be 2 or + and she "
                                          f"is {int(requests.__version__[:1])} ({requests.__version__}) do pip(3) i"
                                          f"nstall requests --upgrade")
    if int(__new_max_version__) > int(__new_version__):
        print(colorama.Fore.RED + f"Your version of CocoyoyoLibrairie API isn't the max version, she is {__version__} a"
                                  f"nd she can be {str(__max_version__)}, pip install cocoyoyo-librairie-api --upgrade "
                                  f"for upgrade" + colorama.Fore.RESET)
    elif int(__new_max_version__) < int(__new_version__) and int(requests.__version__[:1]) > 2:
        pass
