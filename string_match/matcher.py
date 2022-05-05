def naive_string_matcher(text, pattern):
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

def finite_automaton_matcher2(text, pattern):
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
                print(f"{lps}, {i}, {pattern[i]}")
                lps = dfa[lps][pattern[i]]

        return dfa

    transition_func = compute_transition_func()

    state = 0
    for i in range(n): # O(n)
        state = transition_func[state][text[i]]
        if state == m:
            print(f"Pattern occurs with shift {i - m + 1}")

finite_automaton_matcher2("abababacaba", "ababaca")
