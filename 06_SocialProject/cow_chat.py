import cowsay
import asyncio

clients = {}
free_cows_names = cowsay.list_cows()

async def chat(reader, writer):
    reg = False
    me = ""
    clients[me] = asyncio.Queue()
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(clients[me].get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                msg = q.result().decode().split()
                if (len(msg) < 1):
                    continue
                elif (msg[0] == 'who'):
                    keys = ""
                    if len(clients) > 1:
                        for key, val in clients.items():
                            if (key != ""):
                                keys += key + ', '
                    writer.write(f"Registered users: {keys[:-2]}\n".encode())
                    await writer.drain()
                elif (msg[0] == 'cows'):
                    writer.write(f"Free cow names: {', '.join(free_cows_names)}\n".encode())
                    await writer.drain()
                elif (msg[0] == 'login' and not(reg)):
                    if (msg[1] in free_cows_names):
                        me = msg[1]
                        clients[me] = asyncio.Queue()
                        free_cows_names.remove(msg[1])
                        writer.write(f"You are registered with name {me}\n".encode())
                        await writer.drain()
                        reg = True
                        receive.cancel()
                        receive = asyncio.create_task(clients[me].get())
                    else:
                        writer.write("Name is taken or not in list!\n".encode())
                        await writer.drain()
                elif (msg[0] == "say"):
                    if (not(reg)):
                        writer.write("You are not registered!\n".encode())
                        await writer.drain()
                        continue
                    if (msg[1] not in clients.keys()):
                        writer.write(f"The user named {msg[1]} does not exist.\n".encode())
                        await writer.drain()
                        continue
                    else:
                        await clients[msg[1]].put(f"Sender: {me}\n {cowsay.cowsay((' '.join(msg[2:])).strip(), cow=me)}")
                        writer.write("Message send!\n".encode())
                        await writer.drain()
                elif (msg[0] == 'yield'):
                    if (not(reg)):
                        writer.write("You are not registered!\n".encode())
                        await writer.drain()
                        continue
                    else:
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(f"Sender: {me}\n {cowsay.cowsay(' '.join(msg[1:]).strip(), cow=me)}")
                        writer.write("Message send!\n".encode())
                        await writer.drain()
                elif (msg[0] == "quit"):
                    send.cancel()
                    receive.cancel()
                    if reg:
                        print("Quited: ", me)
                        del clients[me]
                        free_cows_names.append(me)
                    writer.close()
                    await writer.wait_closed()
                    return
                else:
                    writer.write("Wrong command!\n".encode())
                    await writer.drain()
            elif (q is receive and reg):
                receive = asyncio.create_task(clients[me].get())
                writer.write(f"{q.result()}\n".encode())
                await writer.drain()
    send.cancel()
    receive.cancel()
    print("Quited: ", me)
    del clients[me]
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())
