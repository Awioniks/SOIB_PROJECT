# /bin/python3

from .in_out_route import In_Out_Route


class Division_Route(In_Out_Route):
    """
    Class which handle Imput and out routing algorithm
    for commutatos
    """
    @classmethod
    def hello(cls) :
        print(cls.research(10, 20))

