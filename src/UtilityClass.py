class Utility(object):

    def __getitem__(self, item):
        return getattr(self, item)

    def placeholderResolve(self, originalString, destinationString):
        print("Utility :: placeholderResolve method :: {}, {}".format(originalString, destinationString))
        if not destinationString:
            return False
        returningString = originalString.replace('*placeholder*', destinationString)
        return returningString