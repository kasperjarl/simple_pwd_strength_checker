from pathlib import Path
import math

class Match:
    def __init__(self, passwordlist='password_lists/10-million-password-list-top-1000000.txt') -> None:
        # sets password list
        self.pwdList = Path(passwordlist)
        self.pwdListContents = self.pwdList.read_text()
        self.pwdLines = self.pwdListContents.splitlines()

        ### Gets passwords and do stuff to it
        print("This will check the strenght of your password")
        print("Will also check if the password is in SecLists top 10 million common passwords")

        self.pwd = input('\nWhat password do you want to check: ')

    def pwd_info(self):
            self.uppercase = False
            self.lowercase = False
            self.numbers = False
            self.special_char = False
            
            self.in_pwd_list = False
            self.exact_match_pwd_list = False
            self.exact_match_line_num = 0
            
            for char in self.pwd:
                if char.isupper():
                    self.uppercase = True
                elif char.islower():
                    self.lowercase = True
                elif not char.isalnum():
                    self.special_char = True
                elif char.isdigit():
                    self.numbers = True

            # Checks if pwd is in password list:
            for line in self.pwdLines:
                self.exact_match_line_num += 1
                if line in self.pwd:
                    self.in_pwd_list = True
                    if line == self.pwd:
                        self.exact_match_pwd_list = True
                        return
                    
class Score(Match):
    def __init__(self) -> None:
        super().__init__()
        self.possible_chars = 0
        self.possible_combinations = 0
        self.cracking_time = 0

        ### Adversary / pwd crackers settings
        ### source: https://x.com/hashcat/status/1095807014079512579 
        self.pwd_crackers_tries_sec = 100_000_000_000
        
    def get_possible_chars(self):
        lowercase = 26
        uppercase = 26
        numbers = 10
        special_chars = 16

        if self.lowercase:
            self.possible_chars += lowercase
        if self.uppercase:
            self.possible_chars += uppercase
        if self.numbers:
            self.possible_chars += numbers
        if self.special_char:
            self.possible_chars += special_chars

        print(f"Possible characters: {self.possible_chars}")

    def get_possible_combinations(self):
        self.possible_combinations = self.possible_chars**len(self.pwd)
        print(f"Possible combinations: {self.possible_combinations}")

    def get_bit(self):
        # ld(possible_combinations^length_of_pwd) ld = dual logarithm
        bit = math.log2(self.possible_combinations)
        formatted_value = "{:.2f}".format(bit)
        print(f"bit: {formatted_value}")


    def time_to_crack(self):
        if not self.exact_match_pwd_list:
            self.cracking_time = (self.possible_combinations 
                                / self.pwd_crackers_tries_sec)
        
        if self.exact_match_pwd_list:
            print(f"\n!!!! Exact match found in SecList Top 10 million passwords !!!!\n")
            self.cracking_time = self.exact_match_line_num / self.pwd_crackers_tries_sec

    def pretty_time(self):
        second = 1
        minute = second * 60
        hour = minute * 60
        day = hour * 24
        month = (day * 365) / 12
        year = month * 12

        if self.cracking_time < minute:
            formatted_value = "{:.10f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} seconds")
            print("\nYou should definetly choose a different password")
            
        elif self.cracking_time >= minute and self.cracking_time < hour:
            self.cracking_time /= minute
            formatted_value = "{:.5f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} minutes")
            print("\nYou should definetly choose a different password")
            
        elif self.cracking_time >= hour and self.cracking_time < day:
            self.cracking_time /= hour
            formatted_value = "{:.2f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} hours")
            print("\nYou should definetly choose a different password")
        
        elif self.cracking_time >= day and self.cracking_time < month:
            self.cracking_time /= day
            formatted_value = "{:.1f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} days")
            print("\nYou should definetly choose a different password")
        
        elif self.cracking_time >= month and self.cracking_time < year:
            self.cracking_time /= month        
            formatted_value = "{:.1f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} months")
            print("\nConsinder a different password, if you don't change you're password more often than the months to crack.")
            
        elif self.cracking_time >= year and self.cracking_time < year * 100: 
            self.cracking_time /= year
            formatted_value = "{:.1f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} years")
            print("\nYou should be good, but still remember to change password frequently.")

        else:
            self.cracking_time /= (year * 100)
            formatted_value = "{:.0f}".format(self.cracking_time)
            print(f"Time to crack: {formatted_value} centuries")
            print("\nYou're good, but credentials do get leaked, so still remember to change passwords frequently")    


