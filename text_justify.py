class Solution:
    def fullJustify(self, words: List[str], maxWidth: int) -> List[str]:
        res = []
        i = 0
        n = len(words)

        while i < n:
            line_len = len(words[i])
            j = i + 1

            while j < n and line_len + 1 + len(words[j]) <= maxWidth:
                line_len += 1 + len(words[j])
                j += 1
            
            line_words = words[i:j]
            num_words = j - i
            total_spaces = maxWidth - sum(len(w) for w in line_words)

            if j == n or num_words == 1:
                # left justify
                line = ' '.join(line_words)
                line += ' ' * (maxWidth - len(line))
            else:
                # full justify
                spaces_between = num_words - 1
                even_space = total_spaces // spaces_between
                extra = total_spaces % spaces_between

                line = ''
                for k in range(spaces_between):
                    line += line_words[k]
                    # add space to leftmost
                    spaces = even_space + (1 if k < extra else 0)
                    line += ' ' * spaces
                line += line_words[-1] # no space after last word
        
            res.append(line)
            i = j
        
        return res
                
        