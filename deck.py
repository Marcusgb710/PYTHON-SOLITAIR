import random
from os.path import exists
import sys
import pygame
import pickle

class Settings:
    def __init__(self, card_color=(255, 255, 255), path=None):
        self.card_color = pygame.Color(card_color)
        self.card_img_path = path

    def get_card_color(self):
        return self.card_color
    
    def get_card_img_path(self):
        return self.card_img_path


    def set_card_color(self, color:str):
        self.card_color = pygame.Color(color)

    def set_card_img_path(self, path:str):
        self.card_img_path = path 

class Card:
    def __init__(self, suite, value, name,color=None):
        
        self.suite = suite
        self.value = value
        self.name = name
        self.color = ("red" if (self.suite == "♦" or self.suite == "♥") else "black") if color == None else color
        self.card_rect = None
        self.card_color = (255, 255, 255)
        
    def get_card_rect(self):
        return self.card_rect

    def get_card_color(self):
        return self.card_color

    def set_card_color(self, color):
        self.card_color = color

    def set_card_rect(self, rect: tuple):
        self.card_rect = pygame.Rect(rect[0], rect[1], rect[2], rect[3])

    def draw(self, win, font:pygame.font.Font, empty=False):
        color = self.get_card_color()
        card_rect = self.get_card_rect()
        card_name = font.render(str(self.name), 0, ((0,0,0) if self.color == "black" else (255, 0, 0)))
        suite_name = font.render(self.suite, 0, ((0,0,0) if self.color == "black" else (255, 0, 0)))
            
        if empty: 
            pygame.draw.rect(win, color, card_rect, 1)

        else:
            pygame.draw.rect(win, color, card_rect)
            pygame.draw.rect(win, (0,0,0), card_rect, 2)
            win.blit(card_name, (card_rect.left + 5, card_rect.top + (card_name.get_rect().y + 5)))
            win.blit(suite_name, (card_rect.right - 15 , card_rect.top + (suite_name.get_rect().y + 5)))
            win.blit(card_name, (card_rect.right - (15 if self.value != 10 else 20), card_rect.bottom - (card_name.get_rect().y+card_name.get_rect().h + 5)))
            win.blit(suite_name, (card_rect.left + 5 , card_rect.bottom - (suite_name.get_rect().y+suite_name.get_rect().h + 5)))
            # win.blit
    def __str__(self):
        return f"Suite: {self.suite}, Value: {self.value}, Color: {self.color}, card Rect: {self.card_rect}"

class Deck:
    def __init__(self):
        self.diamonds = []
        self.hearts = []
        self.clubs = []
        self.spades = []

    def add_cards(self, value, name):
        self.diamonds.append(Card("♦", value, name))
        self.hearts.append(Card("♥", value, name))        
        self.clubs.append(Card("♣", value, name))
        self.spades.append(Card("♠", value, name))

    def shuffle_deck(self): 
        for i in range(13):
            _i = i +1

            if _i == 1:
                self.add_cards(_i, "A")
            
            elif _i == 11:
                self.add_cards(_i, "J")
            
            elif _i == 12:
                self.add_cards(_i, "Q")
            
            elif _i == 13:
                self.add_cards(_i, "K")
            
            else:
                self.add_cards(_i, _i)
        
        deck = self.hearts + self.diamonds + self.spades + self.clubs
        random.shuffle(deck)
        return deck

    def get_suites(self):
        return self.hearts, self.diamonds, self.clubs, self.spades

class Player:
    def __init__(self):
        self.card_from = None
        self.card_to = None
        self.mouse_x = 0
        self.mouse_y = 0
        self.clicked = 0
    
    def get_mouse_pos(self):
        return self.mouse_x, self.mouse_y
    
    def get_mouse_x(self):
        return self.mouse_x
    
    def get_mouse_y(self):
        return self.mouse_y
    
    def get_clicked(self):
        return self.clicked
    
    def get_input(self):
        return self.card_from, self.card_to

    def set_clicked(self, number):
        self.clicked = number
    
    def set_selection_one(self, card_from):
        self.card_from = card_from
    
    def set_selection_two(self, card_to):
        self.card_to = card_to
    
    def set_input(self, card_from, card_to):
        self.card_from = card_from
        self.card_to = card_to
    
    def set_mouse_pos(self, mouse_x, mouse_y):
        self.mouse_x = mouse_x
        self.mouse_y = mouse_y
    
    def pick_card_collection(self, game, card_from, card_to):
        from_collection = None
        to_collection = None
        _card_from = card_from
        _card_to = card_to
        board = game.get_board()
        side_deck = game.get_side_deck()
        suite_collection = game.get_suite_collection()
        

        if _card_from[:4] =="side":
            from_collection = side_deck[0]
            _card_from = _card_from[-1]
            

        elif _card_from[:2] =="sd":
            from_collection = suite_collection
            _card_from = _card_from[-1]
        else:
            from_collection = board

        
        if _card_to[:4] =="side":
            to_collection = side_deck[0]
        elif _card_to[:2] =="sd":
            to_collection = suite_collection
            _card_to = _card_to[-1]
        
        else:
            to_collection = board
        
        if to_collection == board:
            _card_to = card_to[0]

        if from_collection == board:
            return from_collection, to_collection, _card_from[1], _card_to, _card_from[0]
        
        
        return from_collection, to_collection, _card_from, _card_to, None    

    def change_card(self, game):
        card_from, card_to = self.get_input()
        from_collection, to_collection, card_from, card_to, idx = self.pick_card_collection(game, card_from, card_to)
        game.change_card_col(from_collection, to_collection, card_from, card_to, idx)    

    def get_player_input(self, game):
        card_from = input("Enter the column you want to switch the card from: ")
        card_to = input("Enter the column you want to switch the card to: ")
        

        self.set_input(card_from, card_to)
        self.change_card(game)
    
    def change_card_color(self, _collection,  _value, idx=None):
        card_from, card_to = self.get_input()
        collection = _collection
        value = _value
        index = idx

    def click_event(self, game,value):
        card_from, card_to = self.get_input()
        
        
        if card_from == None:
            self.set_selection_one(value)
        if card_from != None and card_to == None:
            self.set_selection_two(value)
            self.change_card(game)
            
            self.set_input(None, None)

    def click_handle(self, card, event):
        _event = event 
        x, y = _event.pos[0], _event.pos[1]

        if x > card.get_card_rect().left and x < card.get_card_rect().right:
            if y > card.get_card_rect().top and y < card.get_card_rect().top + 25:
                return True

        return False

    def handle_deck_click(self, game, event):
        board = game.get_board()
        _event = event
        card_from, card_to = self.get_input()

        for col in board:
            if col:
                if col[0].get_card_rect().collidepoint((_event.pos[0], _event.pos[1])):
                    self.click_event(game,f"{board.index(col)}{0}")
                    if card_from == None:
                        card = board[board.index(col)][0]
                        card.set_card_color((0,0,0))
                    
                else:
                    for card in col:
                        if self.click_handle(card, _event):
                            self.click_event(game,f"{board.index(col)}{col.index(card)}")
                            if card_from == None:
                                card = board[board.index(col)][col.index(card)]
                                card.set_card_color((0,0,0))

    def handle_side_deck_click(self, game, event, shuffle_card: Card):
        side_deck = game.get_side_deck()[0]
        cards_shown = side_deck[0:3]
        _event = event
        _shuffle_card = shuffle_card

        for card in cards_shown:
            if card.get_card_rect().collidepoint((_event.pos[0], _event.pos[1])):
                
                self.click_event(game,f"side{side_deck.index(card)}")
                
                


            if _shuffle_card.get_card_rect().collidepoint((_event.pos[0], _event.pos[1])):
                side_deck.remove(card)
                side_deck.append(card)
    
    def handle_collections_click(self, game, game_gui, event):
        collections_group = game.get_suite_collection()
        
        _event = event

        for collection in collections_group:
            if collection:
                
                for card in collection:
                        
                    if card.get_card_rect().collidepoint((_event.pos[0], _event.pos[1])):
                        self.click_event(game,f"sd{collections_group.index(collection)}")
                        return

    def set_player_controls(self, game, game_gui, shuffle_card: Card):
        back_button = game_gui.get_back_button()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                
                if back_button.rect.collidepoint(event.pos[0], event.pos[1]):
                    main()
                    

                self.handle_deck_click(game, event)
                self.handle_side_deck_click(game, event, shuffle_card)
                self.handle_collections_click(game, game_gui, event)

class Solitare:
    def __init__(self, deck):
        self.board = [[] for i in range(7)]
        self.side_deck=[]
        self.winning_suite = [[] for i in range(4)]
        self._deck = deck
        self.deck = self._deck.shuffle_deck()
        self.check_list = []
        
    def get_board(self):
        return self.board
    
    def get_side_deck(self):
        return self.side_deck
    
    def get_suite_collection(self):
        return self.winning_suite
    
    def get_check_list(self):
        return self.check_list

    def set_check_list(self, check_list):
        self.check_list = check_list

    def set_side_deck(self, side_deck):
        self.side_deck = side_deck

    def set_board(self, board):
        self.board = board

    def set_suite_collection(self, suite):
        self.winning_suite = suite

    def print_board(self):
        board = self.get_board()
        i = 0
        for col in board:
            if len(col) == 0:
                print("EMPTY")
            else:
                print(i, col[0], len(col))
                i += 1

    def print_suite_collection(self):
        suite_collection = self.get_suite_collection()
        i = 0
        for col in suite_collection:
            if len(col) == 0:
                print("EMPTY")
            else:
                print(i, col[0], len(col))
                i += 1
    
    def print_side_deck(self):
        side_deck = self.get_side_deck()
        if len(side_deck) == 0:
            print("EMPTY")
        else:
            i = 0
            for col in side_deck[0]:
                print(i, col)
                i += 1
    
    def populate_board(self):
        board = self.get_board()
        side_deck = self.get_side_deck()
        i = 1
        k = 0
        for col in board:
            for _ in range(i):
                col.append(self.deck[k]) 
                k += 1
            if i == 7:
                side_deck.append(self.deck[k:len(self.deck)])
            i += 1

        self.set_side_deck(side_deck)
        self.set_board(board)

    def is_valid_move(self, from_collection, to_collection, col_num_from, col_num_to, idx=None):
        board = self.get_board()
        suite_collection = self.get_suite_collection()
        side_deck = self.get_side_deck()[0]   
        counter = 0
        
        try:

            if from_collection == side_deck and to_collection == side_deck:
                pass

        #check if the multiple card values below the one selected are decremental 
            if idx != None:
                move_list = from_collection[idx][0:col_num_from+1]
                if len(move_list) > 1:
                    for card in move_list:
                        if counter != 0:
                            if not(card.value-1 == move_list[counter-1].value):
                                return False
                        counter += 1

            #check if user trys to put a card in the suite collection deck
            if to_collection == suite_collection:
                #checks if the first card moved into the suite deck is the valid first card
                if from_collection == side_deck and from_collection[col_num_from].name == "A":
                    return True
                elif idx != None and from_collection == board and from_collection[idx][col_num_from].name == "A":
                    return True
                
                #checks if user moves card from side deck to suite collection
                if from_collection == side_deck and from_collection[col_num_from].value == to_collection[col_num_to][0].value +1 and to_collection[col_num_to][0].suite == from_collection[col_num_from].suite:
                    return True

                #checks if user moves card from board to suite collection
                elif idx != None and from_collection == board and from_collection[idx][col_num_from].value == to_collection[col_num_to][0].value +1 and to_collection[col_num_to][0].suite == from_collection[idx][col_num_from].suite:
                    return True

            #checks of user tries to put a card into an empty slot
            if to_collection[col_num_to][0].value == "":
                if idx != None and from_collection == board and to_collection == board and from_collection[idx][col_num_from].value == 13:
                    return True

                if from_collection == side_deck and to_collection == board and from_collection[col_num_from].value == 13:
                    return True
                
                if from_collection == suite_collection and to_collection == board and to_collection[col_num_to][0].value == 13:
                    return True
                return False

            #checks if user trys to move a card onto the main board from the suite collection
            if from_collection == suite_collection and to_collection == board and to_collection[col_num_to][0].value > from_collection[idx][0].value and from_collection[idx][0].value==to_collection[col_num_to][0].value+1:
                return True

            #checks if user tries to move a card onto the board from the side deck
            if from_collection == side_deck and to_collection == board and from_collection[col_num_from].value < to_collection[col_num_to][0].value and from_collection[col_num_from].value+1==to_collection[col_num_to][0].value:
                return True

            #checks if user moves a card on the board to a different position onto said board
            if idx != None and from_collection == board and to_collection == board and from_collection[idx][col_num_from].value < to_collection[col_num_to][0].value and from_collection[idx][col_num_from].value+1==to_collection[col_num_to][0].value:
                return True
            return False
        except Exception as err:
            print("EXCEPTION ERROR: AUTO DEFAULT ERROR:", err)
            return False

    def change_card_col(self, from_collection, to_collection, col_num_from, col_num_to, col_idx=None):
        board = self.get_board()
        winning_suite = self.get_suite_collection()
        side_deck = self.get_side_deck()
        
        if side_deck[0] == to_collection:
            return
        
        col_num_from = int(col_num_from)
        col_num_to = int(col_num_to)
        col_idx = int(col_idx) if col_idx != None else None
        
        if self.is_valid_move(from_collection, to_collection, col_num_from, col_num_to, col_idx):
            
            # from_collection[col_num_from].remove(card) if (from_collection == board or from_collection == winning_suite and len(from_collection) > 0) else from_collection.remove(card)
            if from_collection == board and col_idx != None:
                card = from_collection[col_idx][col_num_from]
                if col_num_from > 0:
                    for card in list(reversed(from_collection[col_idx][:col_num_from+1])):
                        from_collection[col_idx].remove(card)
                        to_collection[col_num_to].insert(0, card)
                else:        
                    from_collection[col_idx].remove(card)
                    to_collection[col_num_to].insert(0, card)
                
            elif from_collection == board or from_collection == winning_suite and len(from_collection) > 0:
                card = from_collection[col_num_from][0]
                from_collection[col_num_from].remove(card)
                to_collection[col_num_to].insert(0, card)
            else:
                card = from_collection[col_num_from]
                from_collection.remove(card)
                to_collection[col_num_to].insert(0, card)
            pygame.display.update() 

    def win(self):    
        suite_collection = self.get_suite_collection()
        hearts, diamonds, clubs, spades = self._deck.get_suites()
        check_list = self.get_check_list()
        
        _check_list = [(True, "♥"), (True, "♦"), (True, "♣"), (True, "♠")]

        if len(check_list) == 4:
            _check_list = list(sorted(_check_list))
            check_list = list(sorted(check_list))

            if check_list == _check_list:
                    
                    return True

        for _collection in suite_collection:
            collection = list(reversed(_collection[:-1]))
            if len(collection) > 0:
                
                if collection[0].suite == "♥":
                    # print([str(card) for card in collection])
                    coll = [card.suite for card in collection]
                    comp = [card.suite for card in hearts]
                    
                    if coll == comp:
                        comp_result = (True, "♥")
                        
                        if comp_result not in check_list:
                            check_list.append(comp_result)
                
                if collection[0].suite == "♠":
                    coll = [card.suite for card in collection]
                    comp = [card.suite for card in spades]
                    if coll == comp:
                        comp_result = (True, "♠")
                        
                        if comp_result not in check_list:
                            check_list.append(comp_result)


                if collection[0].suite == "♣":
                    coll = [card.suite for card in collection]
                    comp = [card.suite for card in clubs]
                    if coll == comp:
                        comp_result = (True, "♣")

                        if comp_result not in check_list:
                            check_list.append(comp_result)

                if collection[0].suite == "♦":
                    coll = [card.suite for card in collection]
                    comp = [card.suite for card in diamonds]

                    if coll == comp:
                        comp_result = (True, "♦")
                        
                        if comp_result not in check_list:
                            print(check_list)
                            check_list.append(comp_result)
            
        return False

class Button:
    def __init__(self, x, y, width, height, color=(255, 255, 255), text=None):
        self.x = x
        self.y = y
        self. width = width
        self.height = height
        self.color = color
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.text = text

    def get_rect(self):
        return self.rect
    
    def get_text(self):
        return self.text
    
    def set_color(self, color):
        self.color = color

    def draw(self, window: pygame.display, font:pygame.font.Font):
        text = font.render("This is some text", 0, (0,0,0)) if self.text == None else font.render(self.text, 0, (0,0,0))
        pygame.draw.rect(window, self.color, self.rect)
        pygame.draw.rect(window,(0,0,0) , (self.rect.x, self.rect.y, self.rect.width+1, self.rect.height+1),1)
        window.blit(text, (self.rect.centerx - (text.get_rect().w//2), self.rect.centery - (text.get_rect().h//2)))
    
    def clicked(self, event):
        rect = self.get_rect()

        if event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos[0], event.pos[1]):

                return True
            return

    
    def hover(self):
        rect = self.get_rect()
        _mx, _my = pygame.mouse.get_pos()
        mx, my = (_mx,_my)
        
        if  rect.collidepoint(mx, my):
            self.set_color((155, 155, 155))

        else:   
            self.set_color((255, 255, 255))

class Window:
    FPS = 60
    def __init__(self):
        pygame.init()
        self.width = 825
        self.height = 700
        self.window_dimensions = (self.width, self.height)
        self.window = pygame.display.set_mode(self.window_dimensions)
        self.background_color = (150, 255, 200)
        self.font = pygame.font.SysFont("Arial", 20)
        self.clock = pygame.time.Clock()

    def get_height(self):
        return self.height

    def get_width(self):
        return self.width

    def get_window(self):
        return self.window

    def get_background_color(self):
        return self.background_color

    def get_font(self):
        return self.font

    def get_clock(self):
        return self.clock
    
    def get_fps(self):
        return self.FPS
    
    def set_width(self, width):
        self.width = width

    def set_window(self, window):
        self.window = window

    def set_font(self, font):
        self.font = font

    def set_height(self, height):
        self.height = height
    
    def set_background_color(self, color):
        self.background_color = color
    
    def set_clock(self, clock):
        self.clock = clock

class Game(Window):
    def __init__(self):
        super().__init__()
        self.card_width = 75
        self.card_height = 100
        self.side_deck_start = 0
        self.side_deck_end = 3
        self.empty_suite_collection = [Card("", "", "") for i in range(4)]
        self.back_button = Button(10, self.get_height()-45, 80, 40, text="Back")

    def get_card_width(self):
        return self.card_width

    def get_card_height(self):
        return self.card_height

    def get_side_deck_dimensions(self):
        return self.side_deck_start, self.side_deck_end

    def get_empty_suite_collection(self):
        return self.empty_suite_collection

    def get_back_button(self):
        return self.back_button

    def set_card_width(self, width):
        self.card_width = width

    def set_card_height(self, height):
        self.card_height = height

    def set_side_deck_dimension(self, start, end):
        self.side_deck_start = start
        self.side_deck_end = end

    def set_empty_suite_collection(self, empty_suite_collection):
        self.empty_suite_collection = empty_suite_collection

    def set_back_button(self, button):
        self.back_button = button

    def draw_board(self, game: Solitare, _settings: Settings):
        board = game.get_board()
        font = self.get_font()
        window_width = self.get_width()
        card_width, card_height = self.get_card_width(), self.get_card_height()
        window = self.get_window()
        settings = _settings
        card_color = settings.get_card_color()
        x = 75
        y = 165

        for col in board:
            if col:
                y = 165
                for card in list(reversed(col)):
                    card.set_card_rect((x, y, card_width, card_height))
                    if card.suite == "":
                        card.set_card_color(card_color)
                        card.draw(window, font, empty=True)
                    else:
                        card.set_card_color(card_color)
                        card.draw(window, font)
                    if not(card.suite== ""):
                        y += 25
                    
            else:
                c = Card("", "","")
                c.set_card_rect((x, y, card_width, card_height))
                col.append(c)
            x += 100
            
    def draw_side_deck(self, game: Solitare, card: Card, _settings: Settings):
        side_deck = game.get_side_deck()[0]
        font = self.get_font()
        card_width, card_height = self.get_card_width(), self.get_card_height()
        window = self.get_window()
        settings = _settings
        card_color = settings.get_card_color()
        card_show_start, card_show_end = self.get_side_deck_dimensions()
        cards_shown = side_deck[card_show_start: card_show_end]
        shuffle_card = card                                                                                                                                                                                                                                
        x = 475
        y = 10
        
        for card in side_deck:
            card.set_card_rect((0, 0, card_width, card_height))
        for card in cards_shown:
            card.set_card_rect((x, y, card_width, card_height))
            card.set_card_color(card_color)
            card.draw(window, font)

            x += 80

        shuffle_card.set_card_rect((725, y, card_width, card_height)) 
        shuffle_card.set_card_color(card_color)          
        shuffle_card.draw(window, font)

    def draw_collections_decks(self, game: Solitare, _settings: Settings):
        collections_deck = game.get_suite_collection()
        font = self.get_font()
        card_width, card_height = self.get_card_width(), self.get_card_height()
        window = self.get_window()
        settings = _settings
        card_color = settings.get_card_color()
        empty_collection = self.get_empty_suite_collection()


        x = 10
        y = 10
        
        for collection in collections_deck:
            if collection:
                for card in list(reversed(collection)):
                    card.set_card_rect((x, y, card_width, card_height))
                    if not(card.suite == ""):
                        card.set_card_color(card_color)
                        card.draw(window, font)
                    else:
                        card.set_card_color(card_color)
                        card.draw(window, font, empty=True)
                   
            else:
                c=Card("","","")
                c.set_card_rect((x, y, card_width, card_height))
                collection.append(c)
            x+= 80

    def redraw(self, game: Solitare,  shuffle_card: Card, _settings:Settings):
        window = self.get_window()
        settings= _settings
        back_button = self.get_back_button()
        font = self.get_font()
        clock = self.get_clock()
        fps = self.get_fps()

        clock.tick(fps)
        
        background_color = self.get_background_color()
        window.fill(background_color)

        back_button.hover()
        back_button.draw(window, font)

        self.draw_board(game, settings)
        self.draw_side_deck(game, shuffle_card, settings)
        self.draw_collections_decks(game, settings)

    

        pygame.display.update()

class SettingsMenu(Window):
    def __init__(self):
        super().__init__()
        self.buttons_list = []
        self.color_list = ["Light Grey", "Dark Grey", "White", "Dark Sea Green", "Golden Pee", "Blanched Almond",
         "Lavender", "Bubblegum", "Orange Cream", "Pregnancy Scare Blue", "Thistle", "Rosy Brown", "Peach Puff", 
         "Lavender Blush"]

    def get_buttons_list(self):
        return self.buttons_list
    
    def get_color_list(self):
        return self.color_list
    
    def set_buttons_list(self, buttons_list):
        self.buttons_list = buttons_list
    
    def set_color_list(self, color_list):
        self.color_list = color_list

    def switch_card_color(self, _color):
        color = _color
        match color:

            case "Light Grey":
                return (211,211,211)
            
            case "Dark Grey":
                return(169,169,169)
            
            case "Dark Sea Green":
                return (143,188,143)

            case "Golden Pee":
                return (187, 187, 119)

            case "Blanched Almond":
                return (255,235,205)

            case "Lavender":
                return (230,230,250)

            case "Bubblegum":
                return (255, 193, 204)
            
            case "Orange Cream":
                return (255, 198, 179)
            
            case "Pregnancy Scare Blue":
                return (0,113,189)
            
            case "Thistle":
                return (216, 191, 216)
            
            case "Rosy Brown":
                return (188, 143, 143)

            case "Peach Puff":
                return (255,218,185)

            case "Lavender Blush":
                return (255,240,245)

            case _:
                return (255, 255, 255)
    
    def redraw(self, event, _settings:Settings, _settings_menu):
        window = self.get_window()
        bg_color = self.get_background_color()
        settings = _settings
        settings_menu = _settings_menu
    
        window.fill(bg_color)
        
        self.draw_buttons()
        self.handle_button_click(event, settings, settings_menu)
        
        
        pygame.display.update()
    
    def create_buttons(self):
        buttons_list = self.get_buttons_list()
        colors_list = self.get_color_list()
        back_button = Button(10, self.get_height() - 80, 805, 70, text="Back")
        buttons_list.append(back_button)

        x = 25
        y = 25
        for color in colors_list:
            if y + 140 > self.get_height():
                x += 160
                y = 25
            buttons_list.append(Button(x, y, 150, 70, text=color))
            y += 80

    def draw_buttons(self):
        buttons_list = self.get_buttons_list()
        window = self.get_window()
        font = self.get_font()

        if buttons_list:
            for button in buttons_list:
                button.draw(window, font)  

    def handle_button_click(self, _event, _settings:Settings, _settings_menu):
        buttons_list = self.get_buttons_list()
        event = _event
        settings = _settings
        settings_menu = _settings_menu
        

        if buttons_list:
            for button in buttons_list:
                

                if button.clicked(event):
                    if button.text == "Back":
                        save(settings)
                        del settings_menu
                        main()
                        
                    color = self.switch_card_color(button.get_text())
                    settings.set_card_color(color)

    def handle_button_hover(self):
        buttons_list = self.get_buttons_list()
        
        for button in buttons_list:
            button.hover()

    def main(self, settings:Settings, _settings_menu):
        settings_menu = _settings_menu
        clock = self.get_clock()
        fps = self.get_fps()
    
        clock.tick(fps)
        
        self.handle_button_hover()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

            self.redraw(event, settings, settings_menu)

class WinScreen(Window):
    def __init__(self):
        super().__init__()
        self.play_button = None
        self.main_menu_button = None
        self.exit_button = None

    def get_play_button(self):
        return self.play_button

    def get_main_menu_button(self):
        return self.main_menu_button

    def get_exit_button(self):
        return self.exit_button

    def set_exit_button(self, button):
        self.exit_button = button

    def set_play_button(self, button):
        self.play_button = button

    def set_main_menu_button(self, button):
        self.main_menu_button = button

    def redraw(self):
        window = self.get_window()
        font = self.get_font()
        background_color = self.get_background_color()
        _font = pygame.font.SysFont("comicsans", 100)

        window.fill(background_color)

        play_button = self.get_play_button()
        main_menu_button = self.get_main_menu_button()
        exit_button = self.get_exit_button()

        play_button.hover()
        main_menu_button.hover()
        exit_button.hover()

        play_button.draw(window, font)
        main_menu_button.draw(window, font)
        exit_button.draw(window, font)

        win_text = _font.render("You Won!!!", 0, (0,0,0))
        
        window.blit(win_text, (window.get_rect().centerx-(win_text.get_rect().w//2), 250))

        pygame.display.update()
    
    def init(self):
        window = self.get_window()
        play_button = Button(30, window.get_rect().centery+100, (window.get_rect().centerx - 5)-30, 70, text="Play Again")
        main_menu_button = Button((window.get_rect().centerx - 5)+10, window.get_rect().centery+100, (window.get_rect().w - 60)-(window.get_rect().centerx -25), 70, text="Main Menu")
        exit_button = Button(30, window.get_rect().centery + 180 ,window.get_rect().width - 60, 70, text="Exit")
        self.set_play_button(play_button)
        self.set_main_menu_button(main_menu_button)
        self.set_exit_button(exit_button)

    def main(self, _solitare, _win_screen, _settings):
        self.init()
        play_button = self.get_play_button()
        main_menu_button = self.get_main_menu_button()
        exit_button = self.get_exit_button()
        solitare = _solitare
        win_screen = _win_screen
        settings = _settings
        clock = self.get_clock()
        fps = self.get_fps()

        clock.tick(fps)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if play_button.clicked(event):
                
                main_game(settings)
                del win_screen
                
            
            if main_menu_button.clicked(event):
                del solitare, win_screen
                main()
                

            if exit_button.clicked(event):
                del solitare, win_screen
                sys.exit()
        
            self.redraw()

class MainMenu(Window):
    def __init__(self):
        super().__init__()
        self.play_button = None
        self.settings_button = None
        self.exit_button = None
        
    def get_play_button(self):
        return self.play_button

    def get_settings_button(self):
        return self.settings_button

    def get_exit_button(self):
        return self.exit_button

    def set_play_button(self, button):
        self.play_button = button

    def set_settings_button(self, button):
        self.settings_button = button

    def set_exit_button(self, button):
        self.exit_button = button

    def redraw(self):
        window = self.get_window()
        bg_color = self.get_background_color()
        font = self.get_font()
        _font = pygame.font.SysFont("comicsans", 100)

        window.fill(bg_color)

        play_button = self.get_play_button()
        settings_button = self.get_settings_button()
        exit_button = self.get_exit_button()
        
        text = _font.render("SOLITARE", 0, (0,0,0))


        window.blit(text, (window.get_rect().centerx - (text.get_rect().w//2), 80))
        play_button.draw(window, font)
        settings_button.draw(window, font)
        exit_button.draw(window, font)

        


        pygame.display.update()
    
    def init(self):
        window = self.get_window()
        play_button = Button(125, window.get_rect().centery, 576, 70, text="Play")
        settings_button = Button(125, window.get_rect().centery+80, 576, 70, text="Settings")
        exit_button = Button(125, window.get_rect().centery+160, 576, 70, text="Exit")
        self.set_play_button(play_button)
        self.set_settings_button(settings_button)
        self.set_exit_button(exit_button)

    def buttons_hover(self):
        

        play_button = self.get_play_button()
        settings_button = self.get_settings_button()
        exit_button = self.get_exit_button()

        play_button.hover()
        settings_button.hover()
        exit_button.hover()

    def main(self, _settings, _main_menu):
        self.init()
        play_button = self.get_play_button()
        settings_button = self.get_settings_button()
        exit_button = self.get_exit_button()
        settings = _settings
        main_menu = _main_menu
        clock = self.get_clock()
        fps = self.get_fps()

        clock.tick(fps)
        
        self.buttons_hover()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            
            if play_button.clicked(event):
                main_game(settings)
            
                del main_menu
            
            if settings_button.clicked(event):
                setting_menu(settings)
                del main_menu
            
            if exit_button.clicked(event):
                del main_menu
                sys.exit()
            
        self.redraw()

def save(save_settings):
    with open(r"settings.solset", "wb") as outfile:
        pickle.dump(save_settings, outfile)

def load():
    with open(r"settings.solset", "rb") as infile:
        return pickle.load(infile)

def win_screen(_solitaire, _settings):
    w = WinScreen()
    solitare = _solitaire
    settings = _settings

    try:
        while True:
            w.main(solitare, w, settings)
    except Exception as err:
        print(err, "from win screen")
        pygame.quit()
        del w

def main_game(_settings):
    s = Solitare(Deck())
    p = Player()
    g = Game()
    
    settings = _settings

    try:
        shuffle_card = Card("", "", "")
        s.populate_board()

        while True:
            if s.win():
                win_screen(s, settings)
                del s, p, g

            p.set_player_controls(s, g,shuffle_card)

            g.redraw(s, shuffle_card, settings)

    except Exception as err:
        print(err, "from main game")
        pygame.quit()
        del s, p, g

def setting_menu(_settings):
    settings = _settings
    
    s = SettingsMenu()
    s.create_buttons()
    
    try:
        while True:
            s.main(settings, s)
            
    except Exception as err:
        
        print(err, "from settings menu")
        del s
        pygame.quit()

def main():
    path_to_save = r"settings.solset"
    settings = Settings() 
    
    if not(exists(path_to_save)):
        settings = Settings()
        
    else: 
        settings = load()
    
    m = MainMenu()
    
    try:
        while True:
            m.main(settings, m)

    except Exception as err:
        print(err, "from main menu")
        save(settings)
        del m, settings
        sys.exit()

main()