import asyncio
import telnetlib3

from questions import questions, congrats, secret_information, secret_information_2


async def get_answer(reader, writer):
    answer = ''
    next_symbol = ''
    while next_symbol not in ('\n', '\r'):
        next_symbol = await reader.read(1)
        writer.echo(next_symbol)
        answer += next_symbol
        print(answer)
    return answer[:-1]


async def shell_old(reader, writer):
    writer.write('\r\nWell hello there. Do you have a code?\r\nType \'exit\' to close connection\r\n')
    code = ''
    while code != 'exit':
        code = await get_answer(reader, writer)
        question, correct_answer, next_task = questions.get(code, (None, None, None))
        if not question:
            writer.write('\r\nHmm that code doesn\'t look familiar. Do you have other code?\r\n')
            continue
        writer.write(f'\r\nOk, now the question is: {question}\r\n')
        answer = ''
        while answer != correct_answer:
            answer = await get_answer(reader, writer)
            if answer == 'exit':
                code = 'exit'
                break
            if answer == correct_answer:
                writer.write(f'\r\nYES!!!\r\nYour next task is: {next_task}\r\nIf you got some new code, feel free to type in\r\n')
            else:
                writer.write(f'\r\nHmm, sorry, but that\'s not quite correct :(\r\n The question is: {question}\r\n')
    writer.close()


async def shell(reader, writer):
    writer.write('\r\n')
    writer.write('HOOORAYYY!\r\n')
    await asyncio.sleep(2)
    writer.writelines(congrats)
    writer.write('\r\n\r\n\r\n')
    writer.write(secret_information)
    for _ in range(6):
        writer.write('.')
        await asyncio.sleep(1)
    writer.write('\r\n')
    writer.write(secret_information_2)
    writer.write('\r\n')
    writer.write('\r\n')
    writer.write('input anything to close connection\r\n')
    await writer.drain()
    await reader.read(1)
    writer.close()

loop = asyncio.get_event_loop()
coro = telnetlib3.create_server(port=23, shell=shell)
server = loop.run_until_complete(coro)
loop.run_until_complete(server.wait_closed())
