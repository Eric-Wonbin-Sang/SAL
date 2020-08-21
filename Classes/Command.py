
class Command:

    def __init__(self, name, function, requires_args, command_help="Help does not exist!"):
        self.name = name
        self.function = function
        self.requires_args = requires_args
        self.help = command_help

    def run(self, arg_list):
        if arg_list == ["help"]:
            return self.help
        if self.function is None:
            return "{} command's function is None".format(self.name)
        if self.requires_args:
            if not arg_list:
                return self.help
            return self.function(arg_list)
        return self.function()
