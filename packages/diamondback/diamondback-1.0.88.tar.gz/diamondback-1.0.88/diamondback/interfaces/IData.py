""" **Description**

        Data interface.

    **Example**

        ::

            from diamondback import IData


            class Test( IData ) :

                def __init__( self ) -> None :

                    super( ).__init__( )

                    self.data = [ ]

            test = Test( )

            test.data = { 'a' : 0.0, 'b' : 1.0 }

    **License**

        `BSD-3C.  <https://github.com/larryturner/diamondback/blob/master/license>`_

        © 2018 - 2021 Larry Turner, Schneider Electric Industries SAS. All rights reserved.

    **Author**

        Larry Turner, Schneider Electric, Analytics & AI, 2018-07-12.

    **Definition**

"""

from diamondback.interfaces.IEqual import IEqual
import typing


class IData( IEqual ) :

    """ Data interface.
    """

    @property
    def data( self ) :

        """ data : typing.Any.
        """

        return self._data

    @data.setter
    def data( self, data : typing.Any ) :

        self._data = data

    def __eq__( self, other : typing.Any ) -> bool :

        """ Equal.

            Arguments :

                other : typing.Any.

            Returns :

                equal : bool.
        """

        return ( ( super( ).__eq__( other ) ) and ( self.data == other.data ) )

    def __init__( self ) -> None :

        """ Initialize.
        """

        super( ).__init__( )

        self._data = None
