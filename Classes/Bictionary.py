
class Bictionary:

    """ Bi-directional dictionary class (this needs a new name...) """

    def __init__(self, init_dict):

        self.init_dict = init_dict
        self.complete_dict = self.get_complete_dict()

    def get_complete_dict(self):
        complete_dict = {}
        for key, value in self.init_dict.items():
            complete_dict[key] = value
            complete_dict[value] = key
        return complete_dict

    def exists(self, search_key):
        return search_key in self.complete_dict

    def find(self, search_key):
        if self.exists(search_key):
            return self.complete_dict[search_key]
        raise UserWarning("'{}' key in Bictionary does not exist".format(search_key))
