from termcolor import colored
from tabulate import tabulate

class Matcher:
    def __init__(self, verbose=False):
        self.set_verbosity(verbose)

    def set_verbosity(self, verbose=False):
        self.__verbose = verbose
        self.__verboseprint = print if self.__verbose else lambda *a, **k:None


    def naive_string_matcher(self, text, pattern):
        """
        Brute-force patttern matching algorithm

        Time complexity:
            best, average and worst case: O(nm)
        """
        n = len(text)
        m = len(pattern)

        # Iterate through all the shift index
        for s in range(n - m + 1): # O(n)
            if pattern == text[s:s + m]: # O(m)
                print(f"Pattern occurs with shift {s}")

    def finite_automaton_matcher(self, text, pattern):
        """
        Finite-automata matching algorithm
        
        Time complexity: O(n + m*|Σ|)
        """
        n = len(text)
        m = len(pattern)

        def compute_transition_func(): 
            # runs at O(m*|Σ|)
            # m : len of pattern, Σ : number of unique characters in the pattern
                
            input_chars = sorted(set(pattern))  # Unique set of input characters of the given pattern    
            lps = 0     # longest prefix suffix

            # Initialize DFA (deterministic finite automata)
            dfa = {
                state: {
                    x: None for x in input_chars
                } 
                for state in range(m + 1)
            }
            
            # Fill entries in first row (state 0)
            for x in input_chars:
                dfa[0][x] = 0
            dfa[0][pattern[0]] = 1

            # Fill entries in other rows (state 1, state 2, ..., state m)
            for i in range(1, m + 1):
                # Copy values from row at index lps, dfa[lps][:]
                for x in input_chars:
                    dfa[i][x] = dfa[lps][x]
                
                if i < m: # if haven't reach final state, m yet
                    # Update the entry of row state i, column pattern[i]
                    dfa[i][pattern[i]] = i + 1

                    # Update lps for next row to be filled
                    lps = dfa[lps][pattern[i]]

            return dfa

        transition_func = compute_transition_func()

        state = 0
        for i in range(n): # O(n)
            state = transition_func[state][text[i]]
            if state == m:
                print(f"Pattern occurs with shift {i - m + 1}")

    def rabin_karp_matcher(self, text, pattern, R, Q):
        """
        Rabin-Karp matching algorithm

        Unlike Naive string matching algorithm, Rabin-Karp doesn't travel through every character in the subtext
        when checking the equality of a sliding window of text to the pattern. Instead, it computes the unique hash
        of the subtext and compares it with the hash of the pattern to check for equality (This process runs in constant time).  

        Time complexity : 
            best & average case : O(n+m)
            worst case : O(nm)

        Parameters
        ----------
        text : str
            string to find pattern in
        pattern : str
            pattern that you want to find in a text
        R : int
            radix; number of characters in the character set (e.g., ASCII => R=256, a-z => R=26, 0-9 => R=10); only ASCII (256) and 0-9 (10) are supported currently.
        Q : int
            a large random prime number (about mn^2, it helps to maintain probability of spurious hit / hash collision to 1/n)
        """

        # Obtain function to convert string into its numerical representation (only supports 0-9, ASCII by now)
        numeric = int if R == 10 else ord

        n = len(text)
        m = len(pattern)

        # Define modular hash function, i.e., (prev_hash * R + text[i]) % Q = new_hash, repeat
        def hash(key):
            key_hash = 0
            for i in range(m):
                prev_key_hash = key_hash
                key_hash = (key_hash * R + numeric(key[i])) % Q
                
                if self.__verbose and i == 0:
                    self.__verboseprint("hashing : (hash * R + text[i]) % Q = hash")
                self.__verboseprint(f"{' ' * 10}{key[0:i + 1]} % {Q} = ({prev_key_hash} * {R} + {numeric(key[i])}) % {Q} = {key_hash}")
            return key_hash

        # Hash the pattern
        self.__verboseprint(f"pattern : {pattern}")
        pattern_hash = hash(pattern)

        # Hash the first m characters of text
        self.__verboseprint(f"\ntext    : {text}")
        subtext_hash = hash(text[0:m])

        # Slide the window from shift 0 to shift n-m (last window of the text)
        for shift in range(n - m + 1):
            # Compare if the current subtext hash is equals to the pattern hash
            if pattern_hash == subtext_hash:
                if pattern == text[shift:shift + m]: # Compare the pattern and subtext character-wisely, O(m)
                    self.__verboseprint(f"MATCH   : => Pattern found at index {shift} to {shift + m}")
                else:
                    self.__verboseprint(f"warning : Spurious hit occurs: pattern = {pattern}, subtext = {text[shift:shift + m]}, hash_collided = {pattern_hash}")
        
            # Perform rolling hashing, i.e., (R * (prev_hash - text[shift] * (R^(m - 1))) + text[shift + m]) % Q = new_hash, repeat
            if shift < n - m:
                prev_subtext_hash = subtext_hash
                subtext_hash = (R * (subtext_hash - numeric(text[shift]) * (R**(m - 1))) + numeric(text[shift + m])) % Q
                if self.__verbose and shift == 0:
                    self.__verboseprint("note    : start rolling hash : (R * (hash - text[shift] * (R^(m - 1))) + text[shift + m]) % Q = hash")
                self.__verboseprint(f"{' ' * (10 + shift)} {text[shift + 1:shift + m + 1]} % {Q} = ({R} * ({prev_subtext_hash} - {numeric(text[shift])} * ({R}^{m - 1})) + {numeric(text[shift + m])}) % {Q} = {subtext_hash}")
        self.__verboseprint("note    : end rolling hash")


    def knuth_morris_pratt_matcher(self, text, pattern):
        """
        Knuth-Morris-Pratt matching algorithm

        Time complexity :
            best, average, and worst case : O(m + n)
        """

        n = len(text)
        m = len(pattern)

        def compute_prefix_function(pattern, m):
            lps = [None for _ in range(m)]
            lps[0] = 0

            length = 0  # Length of the longest prefix that's also a suffix in a substring
            for i in range(1, m):
                while length > 0 and pattern[length] != pattern[i]:
                    length = lps[length - 1]
                if pattern[length] == pattern[i]:
                    length += 1
                lps[i] = length
            self.__verboseprint(tabulate([["j"] + [j for j in range(m)], ["p"] + [char for char in pattern], ["lps"] + lps], tablefmt="grid"), end="\n\n")
            return lps

        # build pi / longest prefix-suffix table which tells at a particular substring of pattern, 
        # what's the length of longest prefix of the substring that's also a suffix 
        self.__verboseprint("Longest prefix-suffix table")
        lps = compute_prefix_function(pattern, m)                   

        # Find pattern
        j = 0                                                       # number of characters matched, pointer for pattern
        for i in range(n):                                          # i: pointer for text
            while j > 0 and pattern[j] != text[i]:
                _maxn = (n - 1) // 10
                for _x in range(0, _maxn + 1):
                    if _x == 0:
                        self.__verboseprint("    ", end="")
                    self.__verboseprint(f"{_x}{' ' * 9}", end="")
                
                self.__verboseprint("\n" + "i : " + "".join(str(_i) if len(str(_i)) == 1 else str(_i)[-1] for _i in range(n)))
                
                self.__verboseprint("t : " + text[0:i - j] + colored(text[i - j:i], 'green', attrs=['bold']) + colored(text[i], 'red', attrs=['bold']) + text[i + 1:n + 1])
                self.__verboseprint("p : " + " " * (i - j) + colored(pattern[0:j], 'green', attrs=['bold']) + colored(pattern[j], 'red', attrs=['bold']) + pattern[j + 1:m + 1])
                self.__verboseprint("j : " + " " * (i - j) + colored("".join(str(_j) for _j in range(j)) , 'green', attrs=['bold']) + (colored(str(j) , 'red', attrs=['bold'])) + "".join(str(_j) for _j in range(j + 1, m)))
                self.__verboseprint(f"j = lps[{j} - {1}] = {lps[j - 1]}", end="\n\n")
                j = lps[j - 1]

            if pattern[j] == text[i]:
                _maxn = (n - 1) // 10
                for _x in range(0, _maxn + 1):
                    if _x == 0:
                        self.__verboseprint("    ", end="")
                    self.__verboseprint(f"{_x}{' ' * 9}", end="")
                
                self.__verboseprint("\n" + "i : " + "".join(str(_i) if len(str(_i)) == 1 else str(_i)[-1] for _i in range(n)))
                
                self.__verboseprint("t : " + text[0:i - j] + (colored(text[i - j:i + 1], 'green', attrs=['bold'])) + text[i+1:n])
                self.__verboseprint("p : " + " " * (i - j) + (colored(pattern[0:j + 1], 'green', attrs=['bold'])) + pattern[j + 1:m + 1])
                self.__verboseprint("j : " + " " * (i - j) + (colored("".join(str(_j) for _j in range(j + 1)) , 'green', attrs=['bold'])) + "".join(str(_j) for _j in range(j + 1, m)), end="\n\n")
                j += 1

            else:
                _maxn = (n - 1) // 10
                for _x in range(0, _maxn + 1):
                    if _x == 0:
                        self.__verboseprint("    ", end="")
                    self.__verboseprint(f"{_x}{' ' * 9}", end="")
                
                self.__verboseprint("\n" + "i : " + "".join(str(_i) if len(str(_i)) == 1 else str(_i)[-1] for _i in range(n)))
                
                self.__verboseprint("t : " + text[0:i - j] + colored(text[i - j:i], 'green', attrs=['bold']) + colored(text[i], 'red', attrs=['bold']) + text[i + 1:n + 1])
                self.__verboseprint("p : " + " " * (i - j) + colored(pattern[0:j], 'green', attrs=['bold']) + colored(pattern[j], 'red', attrs=['bold']) + pattern[j + 1:m + 1])
                self.__verboseprint("j : " + " " * (i - j) + colored("".join(str(_j) for _j in range(j)) , 'green', attrs=['bold']) + (colored(str(j) , 'red', attrs=['bold'])) + "".join(str(_j) for _j in range(j + 1, m)))
                self.__verboseprint(f"j = {j}", end="\n\n")
                
            if j == m:
                print(f"Pattern occurs with shift {i - m + 1}\n")
                j = lps[j - 1]
            


    

    


            


    