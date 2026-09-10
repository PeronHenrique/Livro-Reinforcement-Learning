from Game import Piece

PIECES: list[Piece] = [

    Piece("square_1", """
        X
    """),

    Piece("square_2", """
        XX
        XX
    """),

    Piece("square_3", """
        XXX
        XXX
        XXX
    """),

    Piece("horizontal_2", """
        XX
    """),

    Piece("horizontal_3", """
        XXX
    """),

    Piece("horizontal_4", """
        XXXX
    """),

    Piece("horizontal_5", """
        XXXXX
    """),

    Piece("vertical_2", """
        X
        X
    """),

    Piece("vertical_3", """
        X
        X
        X
    """),    

    Piece("vertical_4", """
        X
        X
        X
	    X
    """),
	
    Piece("vertical_5", """
        X
        X
        X
	    X
	    X
    """),

   Piece("L - 1.1", """
        XX
        X.
    """),

   Piece("L - 1.2", """
        XX
        .X
    """),

   Piece("L - 1.3", """
        .X
        XX
    """),

   Piece("L - 1.4", """
        X.
        XX
    """),

    Piece("L - 2.1", """
        XXX
        X..
        X..
    """),

    Piece("L - 2.2", """
        XXX
        ..X
        ..X
    """),

    Piece("L - 2.3", """
        ..X
        ..X
        XXX
    """),

    Piece("L - 2.4", """
        X..
        X..
        XXX
    """),

    # Piece("T - 1.1", """
    #     XXX
    #     .X.
    #     .X.
    # """),

    # Piece("T - 1.2", """
    #     ..X
    #     XXX
    #     ..X
    # """),

    # Piece("T - 1.3", """
    #     .X.
    #     .X.
    #     XXX
    # """),

    # Piece("T - 1.4", """
    #     X..
    #     XXX
    #     X..
    # """),
]