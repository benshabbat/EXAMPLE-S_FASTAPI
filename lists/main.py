from string_ops import reverse_str,remove_every_third,to_upper,letter_counts_map,remove_vowels


def main_run():
    print(reverse_str("Hello, World!"))
    print(to_upper("Hello, World!"))
    print(remove_vowels("This is an example."))
    print(remove_every_third("This is an example."))
    print(letter_counts_map("This is an example."))


if __name__ == "__main__":
    main_run()