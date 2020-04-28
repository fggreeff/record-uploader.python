class MismatchingRowCount(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MismatchingExtension(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MismatchingValueType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MismatchingLetterType(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)


class MismatchingHeaders(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
