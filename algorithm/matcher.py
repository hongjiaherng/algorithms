from termcolor import colored
from tabulate import tabulate

class Matcher:

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

        # Use modular hash function, i.e., (prev_hash * R + text[i]) % Q = new_hash, repeat
        # Hash the pattern and the first m characters of text
        pattern_hash = 0
        subtext_hash = 0

        for i in range(m):
            pattern_hash = (pattern_hash * R + numeric(pattern[i])) % Q
            subtext_hash = (subtext_hash * R + numeric(text[i])) % Q

        # Slide the window from shift 0 to shift n-m (last window of the text)
        for shift in range(n - m + 1):
            # Compare if the current subtext hash is equals to the pattern hash
            if pattern_hash == subtext_hash:
                if pattern == text[shift:shift + m]: # Compare the pattern and subtext character-wisely, O(m)
                    print(f"MATCH   : => Pattern found at index {shift} to {shift + m}")
                else:
                    print(f"warning : Spurious hit occurs: pattern = {pattern}, subtext = {text[shift:shift + m]}, hash_collided = {pattern_hash}")
        
            # Perform rolling hashing, i.e., (R * (prev_hash - text[shift] * (R^(m - 1))) + text[shift + m]) % Q = new_hash, repeat
            if shift < n - m:
                subtext_hash = (R * (subtext_hash - numeric(text[shift]) * (R**(m - 1))) + numeric(text[shift + m])) % Q
                


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
            return lps

        # build pi / longest prefix-suffix table which tells at a particular substring of pattern, 
        # what's the length of longest prefix of the substring that's also a suffix 
        lps = compute_prefix_function(pattern, m)                   

        # Find pattern
        j = 0                                                       # number of characters matched, pointer for pattern
        for i in range(n):                                          # i: pointer for text
            while j > 0 and pattern[j] != text[i]:
                j = lps[j - 1]

            if pattern[j] == text[i]:
                j += 1
                
            if j == m:
                print(f"Pattern occurs with shift {i - m + 1}\n")
                j = lps[j - 1]
            


    

    


            


    