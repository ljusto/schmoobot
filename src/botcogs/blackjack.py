from discord.ext import commands
import random
import itertools


class Deck:
    def __init__(self, num_decks=1):
        self.deck = []
        self.num_decks = num_decks
        # self.suites = ["♦", "♣", "♥", "♠"]
        self.suites= ["D", "C", "H", "S"]
        self.numbers = ["A", "2", "3", "4", "5", "6",
                        "7", "8", "9","10", "J", "Q", "K"]
        self.deck = self.make_decks(num_decks)

    def make_decks(self, num_decks):
        lst = []
        for i in range(num_decks):
            for suite in self.suites:
                for number in self.numbers:
                    lst.append(number + suite)
        return lst

    def shuffle(self):
        random.shuffle(self.deck)

    def draw(self):
        return self.deck.pop(0)

    def replace(self, card):
        # does not guard against duplicates!
        if len(card) < 2 or len(card) > 3 or card[- 1] not in self.suites or \
                        card[:-1] not in self.numbers:
            return
        self.deck.append(card)


class Blackjack:
    def __init__(self, bot):
        self.bot = bot
        self.bj_sessions = []

    @commands.command(pass_context=True)
    async def blackjack(self, context):
        await self.bot.say("Starting a blackjack session...")
        rules = "Type 'stop' to stop this session.\n" + \
                "Type 'state' to see the state of the game.\n" + \
                "Type any message to start the game.  You may 'hit' or 'stay'."
        await self.bot.say(rules)
        session = BlackjackSession(context.message.author.id,
                                   context.message.channel)
        self.bj_sessions.append(session)
        print(self.bj_sessions)

class BlackjackSession:
    def __init__(self, owner, channel):
        self.decks = Deck(3)
        self.decks.shuffle()
        self.channel = channel
        self.game_owner_id = owner
        self.player_hand = []
        self.house_hand = []
        self.done = False
        self.player_stay = False

    async def message_handler(self, message):
        #  and message.author.id in list(self.hands.keys())
        if message.author.id != bj.bot.user.id and \
                        message.author.id == self.game_owner_id and \
                not self.done:
            if not self.player_hand or not self.house_hand:
                await self.deal("player", message, num_cards=2)
                await self.deal("dealer", message, private=True)
                await self.deal("dealer", message, num_cards=1)
            if str(message.content).lower() == "stop":
                await self.cleanup(message)
            elif str(message.content).lower() == "state":
                await self.show_game_state(message)
            elif str(message.content).lower() == "hit":
                await self.deal("player", message, num_cards=1)
                if self.value(self.player_hand) > 21:
                    await bj.bot.send_message(message.channel, "You busted!")
                    await self.cleanup(message)
                elif self.value(self.player_hand) == 21:
                    await bj.bot.send_message(message.channel,
                                              "Nice! 21! Looks like you win.")
                    await self.cleanup(message)
                else:
                    await self.dealer_turn(message)

                if self.value(self.house_hand) > 21:
                    await bj.bot.send_message(message.channel,
                                              "Looks like I busted. You win!")
                    await self.cleanup(message)
                elif self.value(self.house_hand) == 21:
                    await bj.bot.send_message(message.channel,
                                              "21!! I guess I win!")
                    await self.cleanup(message)

            elif str(message.content).lower() == "stay" and \
                            self.value(self.player_hand) < 21:
                # finish up dealer's turn
                self.player_stay = True
                while await self.dealer_turn(message):
                    pass
                await bj.bot.send_message(message.channel, "I think I'll stay.")
                if self.value(self.house_hand) > 21:
                    await bj.bot.send_message(message.channel,
                                              "Looks like I busted. You win!")
                elif self.value(self.house_hand) == 21:
                    await bj.bot.send_message(message.channel,
                                              "21!! I guess I win!")
                elif self.value(self.house_hand) > self.value(self.player_hand):
                    await bj.bot.send_message(message.channel,
                                              "You got higher than me. You win!"
                                              )
                else:
                    await bj.bot.send_message(message.channel,
                                              "Looks like I got higher! I win!")
                await self.cleanup(message)
                    
    async def cleanup(self, message):
        self.done = True
        await self.show_game_state(message, end=True)
        await bj.bot.send_message(message.channel,
                                  "Now removing our game...Hope you had fun!")
        bj.bj_sessions.remove(self)
        
    async def dealer_turn(self, message):
        """
        Returns true if hit, returns false if not.
        """
        val = self.value(self.house_hand)
        if val < 16 or \
                (self.player_stay and val < self.value(self.player_hand)):
            await bj.bot.send_message(message.channel, "Hit me!")
            await self.deal(self.house_hand, message)
            return True
        else:
            return False

    def value(self, hand):
        """
        Always gravitates towards 21. Returns value of the hand (an integer)
        between 0 and 21.
        """
        value_no_aces = 0
        num_aces = 0
        for card in hand:
            if card[:-1] in "JQK":
                value_no_aces += 10
            elif card[:-1] in "2345678910":
                value_no_aces += int(card[:-1])
            else:
                num_aces += 1
        value = value_no_aces
        mini = 10000000
        best_total = 0
        # generate all possible pairs of n-tuples with elements 1 and 11
        paths = list(itertools.product([1, 11], repeat=num_aces))
        # find the best tuple (closest to 21)
        totals = map(sum, paths)
        for total in totals:
            diff = 21 - (value_no_aces + total)
            if diff == 0:
                return value_no_aces + total
            elif 0 < diff < mini:
                mini = diff
                best_total = total
        # if we haven't set best_total, then we were over 21
        # before we even counted aces
        if best_total == 0:
            best_total = num_aces

        value += best_total
        return value

    async def show_game_state(self, message, end=False):
        """
        Displays the current state of the game
        """
        player_cards = len(self.player_hand)
        house_cards = len(self.house_hand)
        if end:
            result = "__**FINAL STATS:**__\n**Dealer's cards:** "
            for i in range(house_cards):
                result += self.house_hand[i] + ", "
            result = result[:-2] + " (Best value: " + \
                     str(self.value(self.house_hand)) + ")\n**" + \
                     str(message.author) + "'s cards:** "
        else:
            result = "**Dealer's cards:** *, "
            for i in range(1, house_cards):
                result += self.house_hand[i] + ", "
            result = result[:-2] + "\n**" + str(message.author) + "'s cards:** "

        for i in range(player_cards):
            result += self.player_hand[i] + ", "
        result = result[:-2] + " (Best value: " + \
                 str(self.value(self.player_hand)) + ")"
        await bj.bot.send_message(message.channel, result)

    async def deal(self, who, message, private=False, num_cards=1):
        hand = self.player_hand if who == "player" else self.house_hand
        for i in range(num_cards):
            card = self.decks.draw()
            hand.append(card)
            if who == "player":
                result = str(message.author) + " got a "
                if private:
                    result += "*"
                else:
                    result += card
            else:
                result = "schmoobot got a "
                if private:
                    result += "*"
                else:
                    result += card
            await bj.bot.send_message(message.channel, result)


async def get_bj_session_by_userid(userid):
    length = len(bj.bj_sessions)
    for i in range(length):
        if bj.bj_sessions[i].game_owner_id == userid:
            return i
    return -1

async def check_messages(message):
    if message.author.id != bj.bot.user.id:
        if await get_bj_session_by_userid(message.author.id) >= 0:
            index = await get_bj_session_by_userid(message.author.id)
            session = bj.bj_sessions[index]
            if not session.done:
                await session.message_handler(message)


def setup(bot):
    global bj
    bot.add_listener(check_messages, "on_message")
    bj = Blackjack(bot)
    bot.add_cog(bj)



