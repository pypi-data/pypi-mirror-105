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
__version__ = "1.5.0"
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
        self.user_token_link = self.base_link + "user_token:"
        if type(getting_started_message) is not bool:
            raise CocoyoyoLibrairie_Exception('getting_started_message must be boolean')
        if getting_started_message:
            print(CocoyoyoLibrairie.__doc__)

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
            raise CocoyoyoLibrairie_Exception('parm isbn must be str or int')
        try:
            return j_l(g(self.user_token_link + str(token)).content)['views']

        except json.decoder.JSONDecodeError:
            raise CocoyoyoLibrairie_Exception('No User Found With This Token')
        except Exception as e:
            raise CocoyoyoLibrairie_Exception(f'An exception occurred : {e.args}')
        except:
            raise CocoyoyoLibrairie_Exception("An unknown exception occurred, if you can't find a way out please report"
                                              " it on https://github.com/CAMARMFlipz/Cocoyoyo_Librairie_Python_Api/issu"
                                              "es")

    def credits(self):
        """
        CocoyoyoLibrairie Official Python Api By CAMARM-DEV !
        https://www.camarm.dev
        http://www.camarm.fr
        http://www.camponovo.space
        https://cocoyoyo-librairie.camponovo.space
        """
        print(self.credits.__doc__)


class CocoyoyoLibrairie_Exception(Exception):
    """
    Exceptions of CocoyoyoLibrairie API
    """


if __name__ == "cocoyoyo_librairie.api":
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
