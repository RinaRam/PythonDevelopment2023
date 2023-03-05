import shlex
import cmd
import cowsay
import readline


def complete_cowsay_or_cowthink(text, line, begidx, endidx):
	args = shlex.split(line)
	len_args = len(args)
	eyes = ["OO", "XX", "DD", "YY", "QQ", "TT", "UU", "CC", "oo"]
	tongues = ["II", "VV", "U ", "WW", "UU"] 
	if (text == args[-1]):
		len_args -= 1
	if len_args == 2:
		return [c for c in cowsay.list_cows() if c.startswith(text)]
	if len_args == 3:
		return [c for c in eyes if c.startswith(text)]
	if len_args == 4:
	    return [c for c in tongues if c.startswith(text)]

def cowsay_or_cowthink(arg):
	message, *options = shlex.split(arg)
	eyes = 'oo'
	tongue = '  '
	cow = 'default'
	if options:
		if options[0]:
			cow = options[0]
		if (len(options) > 1 and options[1]):
			eyes = options[1]
		if (len(options) > 2 and options[2]):
			tongue = options[2]
	return [message, eyes, tongue, cow]


class Cow_Say_Cmd(cmd.Cmd):
	intro = "Welcome to the cow cmd!\n"
	prompt = "(cow) "

	def do_list_cows(self, arg):
		"""\n  list_cows [dir]\n  Lists all cow file names in the given directory or default cow list\n"""
		if arg:
			print(*cowsay.list_cows(shlex.split(arg)[0]))
		else:
			print(*cowsay.list_cows())

	def do_make_bubble(self, arg):
		"""\n  make_buble [wrap_text [width [brackets ]]]\n  The text that appears above the cows\n"""
		message, *options = shlex.split(arg)
		wrap_text = True
		width = 40
		brackets = cowsay.THOUGHT_OPTIONS['cowsay']
		if options:
			if options[0]:
				wrap_text = bool(options[0] == 'True')
			if (len(options) > 1 and options[1]):
				width = int(options[1])
			if (len(options) > 2 and options[2]):
				brackets = cowsay.THOUGHT_OPTIONS[options[2]]
		print(cowsay.make_bubble(message, brackets=brackets, width=width, wrap_text=wrap_text))

	def complete_make_bubble(self, text, line, begidx, endidx):
		args = shlex.split(line)
		len_args = len(args)
		if ((len_args == 2 and args[-1] != text) or (len_args == 3 and args[-1] == text)):
			return [res for res in ['True', 'False'] if res.lower().startswith(text.lower())]


	def do_cowsay(self, arg):
		"""\n  cowsay message [cow [eyes [tongue]]]\n  Display a message as cow phrases\n"""
		message, eyes, tongue, cow = cowsay_or_cowthink(arg)
		print(cowsay.cowsay(message, eyes=eyes, tongue=tongue, cow=cow))


	def complete_cowsay(self, text, line, begidx, endidx):
		return complete_cowsay_or_cowthink(text, line, begidx, endidx)


	def do_cowthink(self, arg):
		"""\n  cowthink message [cow [eyes [tongue]]]\n  Display a message as cow thoughts\n"""
		message, eyes, tongue, cow = cowsay_or_cowthink(arg)
		print(cowsay.cowthink(message, eyes=eyes, tongue=tongue, cow=cow))

	def complete_cowthink(self, text, line, begidx, endidx):
		return complete_cowsay_or_cowthink(text, line, begidx, endidx)

	def do_exit(self, arg):
		"""\n  Exit cow cmd\n"""
		return True

if __name__ == "__main__":
	Cow_Say_Cmd().cmdloop()
