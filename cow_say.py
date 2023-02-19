import argparse
import cowsay

parser = argparse.ArgumentParser(prog = 'Cowsay',
                                 description='Cow say like program.')


parser.add_argument('-l', 
                    dest='l', 
                    action='store_true', 
                    help='To list all cowfiles on the current COWPATH.',
                    required=False)

parser.add_argument('message',
                    action='store',
                    default='',
                    help='A string to wrap in the text bubble.',
                    nargs='?')


parser.add_argument('-e', 
                    dest='eyes', 
                    action='store', 
                    default='oo',
                    help='',
                    required=False)

parser.add_argument('-f', 
                    dest='cowfile', 
                    action='store', 
                    default='',
                    help='Specifies a particular cow picture file (''cowfile'') to use.',
                    required=False)

parser.add_argument('-n', 
                    dest='wrap_text', 
                    action='store_false', 
                    help='If it is specified, the given message will not be word-wrapped.',
                    required=False)

parser.add_argument('-T', 
                    dest='tongue', 
                    action='store', 
                    default=' ',
                    help='To select the appearance of the cow\'s tongue. It must be two characters and does not appear by default. However, it does appear in the \'dead\' and \'stoned\' modes.',
                    required=False)

parser.add_argument('-W', 
                    dest='width', 
                    action='store', 
                    default=40,
                    type=int,
                    help='Specifies roughly where the message should be wrapped.',
                    required=False)

parser.add_argument('-b', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='b',
                    help='Initiates Borg mode.',
                    required=False)


parser.add_argument('-d', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='d',
                    help='Causes the cow to appear dead.',
                    required=False)

parser.add_argument('-g', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='g',
                    help='Invokes greedy mode.',
                    required=False)

parser.add_argument('-p', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='p',
                    help='Causes a state of paranoia to come over the cow.',
                    required=False)

parser.add_argument('-s', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='s',
                    help='Makes the cow appear thoroughly stoned.',
                    required=False)

parser.add_argument('-t', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='t',
                    help='Yields a tired cow.',
                    required=False)

parser.add_argument('-w', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='w',
                    help='Initiates wired mode.',
                    required=False)

parser.add_argument('-y', 
                    dest='preset', 
                    action='append_const', 
                    default=[''],
                    const='y',
                    help='Brings on the cow\'s youthful appearance.',
                    required=False)


args = parser.parse_args()

if args.l:
    print(cowsay.list_cows())
else:
  cow_tmp = 'default'
  cowfile_tmp = None
  if ('/' in args.cowfile):
    cowfile_tmp = args.cowfile
  elif (args.cowfile in cowsay.list_cows()):
      cow_tmp = args.cowfile
  
  print(cowsay.cowsay(args.message, 
                      cow=cow_tmp, 
                      preset=max(args.preset), 
                      eyes=args.eyes[0:2], 
                      tongue=args.tongue[0:2], 
                      width=args.width, 
                      wrap_text=args.wrap_text, 
                      cowfile=cowfile_tmp
                     )
  )