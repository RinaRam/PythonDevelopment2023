import socket
import readline
import select
import cmd
import shlex
import threading
import sys

thread_lock = threading.Lock()

class ChatClient(cmd.Cmd):
    prompt = '> '

    def __init__(self, s):
        super().__init__()
        self.sock = s

    def send_msg(self, msg):
        self.sock.send(msg.encode())

    def recv_msg(self, timeout):
        readable, _, _ = select.select([self.sock], [], [], timeout)
        for sock in readable:
            msg = sock.recv(1024).decode()
            return msg
        return None

    def do_who(self, args):
        self.send_msg("who\n")

    def do_cows(self, args):
        self.send_msg("cows\n")

    def do_login(self, args):
        self.send_msg(f"login {shlex.split(args)[0]}\n")

    def do_say(self, args):
        self.send_msg(f"say {args.strip()}\n")

    def do_yield(self, args):
        self.send_msg(f"yield {args.strip()}\n")

    def do_exit(self, args):
        self.send_msg("exit\n")
        return True

    def complete_login(self, text, line, begidx, endidx):
        with thread_lock:
            self.send_msg("cows\n")
            msg = self.recv_msg(timeout=None)
            for c in ["'", "[", "]", ","]:
                msg = msg.replace(c, "")
            cows = msg.strip().split()[2:]
            result = []
            for s in cows:
                if s.startswith(text):
                    result.append(s)
            return result

    def complete_send_message(self, text, line, begidx, endidx):
        with thread_lock:
            if len(text.split()) <= 1:
                self.send_msg("who\n")
                msg = self.recv_msg(timeout=None)
                for c in ["'", "[", "]", ","]:
                    msg = msg.replace(c, "")
                who = msg.strip().split()[2:]
                result = []
                for s in who:
                    if s.startswith(text):
                        result.append(s)
                return result

    def start_messaging_thread(self):
        while True:
            with thread_lock:
                msg = self.recv_msg(timeout=0.)
                if msg:
                    print(msg.strip())
                    print(f"{self.prompt}{readline.get_line_buffer()}", end="", flush=True)


if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        if len(sys.argv) > 2:
            sock.connect((sys.argv[1], int(sys.argv[2])))
        else:
            sock.connect((sys.argv[1], 1337))
        sock.setblocking(False)
        client = ChatClient(sock)
        gm = threading.Thread(target=client.start_messaging_thread)
        gm.start()
        client.cmdloop()