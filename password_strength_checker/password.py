import itertools
import string
import time


def check_against_wordlist(password, wordlist_path="rockyou.txt"):
    try:
        with open(wordlist_path, "r", encoding="latin-1") as file:
            for line in file:
                if line.strip() == password:
                    return True
    except FileNotFoundError:
        print(f"Súbor '{wordlist_path}' sa nenašiel, preskakujem kontrolu slovníka.")
    return False


def estimate_bruteforce(password, max_length=5, time_limit_seconds=15):
    charset = string.ascii_lowercase + string.digits

    if len(password) > max_length:
        combinations = len(charset) ** len(password)
        seconds = combinations / 1_000_000_000
        return None, seconds

    start = time.time()
    for length in range(1, max_length + 1):
        for guess_tuple in itertools.product(charset, repeat=length):
            if time.time() - start > time_limit_seconds:
                return False, time.time() - start
            guess = "".join(guess_tuple)
            if guess == password:
                return True, time.time() - start
    return False, time.time() - start


def format_time(seconds):
    if seconds < 1:
        return "menej ako sekundu"
    intervals = [
        ("rok", 31536000),
        ("deň", 86400),
        ("hodinu", 3600),
        ("minútu", 60),
        ("sekundu", 1),
    ]
    for name, count in intervals:
        if seconds >= count:
            value = seconds / count
            return f"~{value:,.1f} {name}(y)"
    return "menej ako sekundu"


def check_strength(password):
    issues = []
    has_letter = any(c.isalpha() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(not c.isalnum() for c in password)

    if len(password) < 8:
        issues.append("príliš krátke (min. 8 znakov)")
    if not has_letter:
        issues.append("chýbajú písmená")
    if not has_digit:
        issues.append("chýbajú čísla")
    if not has_special:
        issues.append("chýbajú špeciálne znaky (!@#$...)")

    return issues


def main():
    password = input("Zadaj heslo, ktoré chceš otestovať: ")

    print("\n1) Kontrola proti slovníku rockyou.txt")
    if check_against_wordlist(password):
        print("Heslo sa nachádza v rockyou.txt - je veľmi bežné a nebezpečné.")
    else:
        print("Heslo sa v rockyou.txt nenašlo.")

    print("\n2) Odhad odolnosti voči brute-force útoku")
    found, seconds = estimate_bruteforce(password)
    if found is True:
        print(f"Heslo by sa dalo uhádnuť brute-force útokom za {format_time(seconds)}.")
    elif found is False:
        print(f"V rámci testovaného limitu ({format_time(seconds)} skúšania) sa heslo neuhádlo.")
    else:
        print(f"Heslo je príliš dlhé na reálne skúšanie. Teoretický odhad času na uhádnutie: {format_time(seconds)}.")

    print("\n3) Kontrola sily hesla")
    issues = check_strength(password)
    if issues:
        print("Heslo je slabé:")
        for issue in issues:
            print(f" - {issue}")
    else:
        print("Heslo vyzerá silno (z hľadiska dĺžky a rozmanitosti znakov).")


if __name__ == "__main__":
    main()
