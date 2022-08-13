import random


def generate_n_random_numbers(quantity):
    return [random.randint(0, 36) for _ in range(quantity)]


if __name__ == '__main__':
    balance = 20
    bet = 0.20

    win = 0
    lose = 0

    quant_number_in_blank = 2

    numbers = generate_n_random_numbers(quant_number_in_blank)

    for _ in range(10):
        balance = 20
        for i in range(30):

            bad_luck_number = generate_n_random_numbers(quant_number_in_blank)

            lucky_number = random.randint(0, 36)

            numbers.append(lucky_number)

            if lucky_number in bad_luck_number:

                balance -= bet * (37 - quant_number_in_blank)
                lose += 1
            else:

                balance += ((bet * 37) - (bet * (37 - quant_number_in_blank)))
                win += 1

        print(f'-------------- Game {_} --------------')
        win_percentage = win / (win + lose)
        print("Win percentage: ", win_percentage)
        print("Balance: ", balance)
        print('-------------------------------------')
        print("\n")