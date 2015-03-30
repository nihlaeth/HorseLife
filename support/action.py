class Action():
    def __init__(self, cls, arguments):
        """ Container class.

        Action acts as a kind of messenger between classes. This results in
        decreased complexity as by simply passing a class and a bunch of
        arguments around, the sender of this action doesn't have to worry
        about initialization, and the return of that initialization can be
        left to the recipient of said action. This is basically delayed
        execution.

        Arguments:
        cls -- class
        arguments -- dict of arguments needed to initialize the class
        """
        self.cls = cls
        self.arguments = arguments
