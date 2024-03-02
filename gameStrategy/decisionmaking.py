def calculate_values(deck: dict, player: list[str], dealer: list[str]) -> tuple[bool, int, int]:
    player_count = player_value = 0
    ace = False

    # player hand value
    for card in player:
        player_count += 1
        if deck[card] == 11 and player_count < 3:
            ace = True
            player_value += deck[card]
        elif deck[card] == 11:
            player_value += 1
        else:
            player_value += deck[card]

    # dealer top value
    dealer_value = deck[dealer[0]]

    return (ace, player_value, dealer_value)

def decision_making(ace: bool, player: int, dealer: int) -> str:
    # soft total
    if ace:
        match player:
            case 20:
                return 'stand'
            case 19:
                if dealer == 6:
                    return 'double'
                else:
                    return 'stand'
            case 18:
                if dealer in range(2, 7):
                    return 'double'
                elif dealer in range(9, 11):
                    return 'stand'
                else:
                    return 'hit'
            case 17:
                if dealer in range(3, 7):
                    return 'double'
                else:
                    return 'hit'
            case 16:
                if dealer in range(4, 7):
                    return 'double'
                else:
                    return 'hit'
            case 15:
                if dealer in range(4, 7):
                    return 'double'
                else:
                    return 'hit'
            case 14:
                if dealer in range(5, 7):
                    return 'double'
                else:
                    return 'hit'
            case 13:
                if dealer in range(5, 7):
                    return 'double'
                else:
                    return 'hit'
    # hard total
    else:
        match player:
            case 17 | 18 | 19 | 20 | 21:
                return 'stand'
            case 16:
                if dealer in range(2, 7):
                    return 'stand'
                else:
                    return 'hit'
            case 15:
                if dealer in range(2, 7):
                    return 'stand'
                else:
                    return 'hit'
            case 14:
                if dealer in range(2, 7):
                    return 'stand'
                else:
                    return 'hit'
            case 13:
                if dealer in range(2, 7):
                    return 'stand'
                else:
                    return 'hit'
            case 12:
                if dealer in range(4, 7):
                    return 'stand'
                else:
                    return 'hit'
            case 11:
                return 'double'
            case 10:
                if dealer in range(2, 10):
                    return 'double'
                else:
                    return 'hit'
            case 9:
                if dealer in range(3, 7):
                    return 'double'
                else:
                    return 'hit'
            case 8 | 7 | 6 | 5 | 4:
                return 'hit'