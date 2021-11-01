import contextlib
import math
import random

#=======================================================================
# Base class
#=======================================================================
class EOFErro(Exception):
    pass


class AsyncConnectionBase:
    def __init__(self, reader, writer):
        self.reader = reader                        # Changed
        self.writer = writer                        # Changed

    async def send(self, command):
        line = command + '\n'
        data = line.encode()
        self.writer.write(data)                     # Changed
        await self.writer.drain()                   # Changed

    async def receive(self):
        line = await self.reader.readline()         # Changed
        if not line:
            raise EOFError('Connection closed')
        return line[:-1].decode()

#=======================================================================
# Server Client
#=======================================================================
WARMER = 'Warmer'
COLDER = 'Colder'
UNSURE = 'Unsure'
CORRECT = 'Correct'


class UnknownCommandError(Exception):
    pass


class AsyncSession(AsyncConnectionBase):       # Changed
    def __init__(self, *args):
        super().__init__(*args)
        self._cleare_state(None, None)

    def _cleare_state(self, lower, upper):
        self.lower = lower
        self.upper = upper
        self.secret = None
        self.gueses = []

    async def loop(self):                       # Changed
        while command := await self.receive():  # Changed
            parts = command.split(' ')
            if parts[0] == "PARAMS":
                self.set_params(parts)
            elif parts[0] == "NUMBER":
                await self.send_number()         # Changed
            elif parts[0] == "REPORT":
                self.receive_report(parts)
            else:
                raise UnknownCommandError(command)

    def set_params(self, parts):
        assert len(parts) == 3
        lower = int(parts[1])
        upper = int(parts[2])
        self._cleare_state(lower, upper)

    def next_guess(self):
        if self.secret is not None:
            return self.secret

        while True:
            guess = random.randint(self.lower, self.upper)
            if guess not in self.gueses:
                return guess

    async def send_number(self):        # Changed
        guess = self.next_guess()
        self.gueses.append(guess)
        await self.send(format(guess))  # Changed

    def receive_report(self, parts):
        assert len(parts) == 2
        decision = parts[1]

        last = self.gueses[-1]
        if decision == CORRECT:
            self.secret = last

        print(f'Server: {last} is {decision}')


class AsyncClient(AsyncConnectionBase):      # Changed
    def __init__(self, *args):
        super().__init__(*args)
        self._clear_state()

    def _clear_state(self):
        self.secret = None
        self.last_distance = None

    @contextlib.asynccontextmanager                    # Changed
    async def session(self, lower, upper, secret):     # Changed
        print(f'Guess a number between {lower} and {upper}! Shhhhh, it\'s {secret}')
        self.secret = secret
        await self.send(f'PARAMS {lower} {upper}')     # Changed
        try:
            yield 
        finally:
            self._clear_state()
            await self.send('PARAMS 0 -1')             # Changed

    async def request_number(self, count):             # Changed
        for _ in range(count):
            await self.send("NUMBER")                  # Changed
            data = await self.receive()                # Changed
            yield  int(data)
            if self.last_distance == 0:
                return

    async def report_outcome(self, number):             # Changed
        new_distance = math.fabs(number - self.secret)
        decision = UNSURE

        if new_distance == 0:
            decision = CORRECT
        elif self.last_distance is None:
            pass
        elif new_distance < self.last_distance:
            decision = WARMER
        elif new_distance > self.last_distance:
            decision = COLDER
        
        self.last_distance = new_distance

        await self.send(f'REPORT {decision}')           # Changed
        # Make it so the output printing is in
        # the same order as the threaded version.
        await asyncio.sleep(0.01)
        return decision


import asyncio

async def handle_async_connection(reader, writer):
        session = AsyncSession(reader, writer)
        try:
            await session.loop()
        except EOFError:
            pass

async def run_async_server(address):
    server = await asyncio.start_server(
        handle_async_connection, *address
    )
    async with server:
        await server.serve_forever()

async def run_async_client(address):
    # Wait for the server to listen before trying to connect
    await asyncio.sleep(0.01)

    streams = await asyncio.open_connection(*address)     # New
    client = AsyncClient(*streams)                        # New

    async with client.session(1, 5, 3):
        results = [(x, await client.report_outcome(x))
                    async for x in client.request_number(5)]
        
    async with client.session(10, 15, 12):
        async for number in client.request_number(5):
            outcome = await client.report_outcome(number)
            results.append((number, outcome))

    _, writer = streams                                   # New
    writer.close()                                        # New
    await writer.wait_closed()                            # New

    return results


async def main_async():
    address = ('127.0.0.1', 1234)

    server = run_async_server(address)
    asyncio.create_task(server)

    results = await run_async_client(address)
    for number, outcome in results:
        print(f'Client: {number} is {outcome}')

loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
