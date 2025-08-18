from collections import Counter
import re
def is_interesting(number, awesome_phrases):
    current_mile = interesting_value(number, awesome_phrases)
    next_mile = interesting_value(number+1, awesome_phrases)
    next_mile_after = interesting_value(number+2, awesome_phrases)
    
    print(f"cur {current_mile} next: {next_mile} next_mile_after: {next_mile_after}")
    if current_mile:
        return 2
    if next_mile or next_mile_after:
        return 1
    return 0
    
def interesting_value(number, awesome_phrases):
    print(f"number - {number}")
    if number < 100:
        return False
    
    s = str(number)

    # any digit followed by 0's
    if re.fullmatch(r'[1-9]0+', s):
        return True
    #same number for every digit
    if len(set(s)) == 1:
        return True
    # Sequential incrementing (9->0)
    if s in "1234567890":
        return True
    # Sequential decreasing (1->0)
    if s in "9876543210":
        return True
    # Palindrome check
    if s == s[::-1]:
        return True
    if number in awesome_phrases:
        return True
    return False

STATE_TO_COMMANDS = {
  'CLOSED': {
    'APP_PASSIVE_OPEN': 'LISTEN',
    'APP_ACTIVE_OPEN': 'SYN_SENT'
  },
  'LISTEN': {
    'RCV_SYN': 'SYN_RCVD',
    'APP_SEND': 'SYN_SENT',
    'APP_CLOSE': 'CLOSED'
  },
  'SYN_RCVD': {
    'APP_CLOSE': 'FIN_WAIT_1',
    'RCV_ACK': 'ESTABLISHED'
  },
  'SYN_SENT': {
    'RCV_SYN': 'SYN_RCVD',
    'RCV_SYN_ACK': 'ESTABLISHED',
    'APP_CLOSE': 'CLOSED'
  },
  'ESTABLISHED': {
    'APP_CLOSE': 'FIN_WAIT_1',
    'RCV_FIN': 'CLOSE_WAIT'
  },
  'FIN_WAIT_1': {
    'RCV_FIN': 'CLOSING',
    'RCV_FIN_ACK': 'TIME_WAIT',
    'RCV_ACK': 'FIN_WAIT_2'
  },
  'CLOSING': {
    'RCV_ACK': 'TIME_WAIT'
  },
  'FIN_WAIT_2': {
    'RCV_FIN': 'TIME_WAIT'
  },
  'TIME_WAIT': {
    'APP_TIMEOUT': 'CLOSED'
  },
  'CLOSE_WAIT': {
    'APP_CLOSE': 'LAST_ACK'
  },
  'LAST_ACK': {
    'RCV_ACK': 'CLOSED'
  }
}


def traverse_TCP_states(events):
  state = "CLOSED"  # initial state, always
  for event in events:
    if event not in STATE_TO_COMMANDS[state]:
      return 'ERROR'
    state = STATE_TO_COMMANDS[state][event]
  return state

def loop_deque(deque):
  score_size = len(deque)
  for _ in range(score_size):
    value, count = deque.popleft()
    if count > 0:
      value = value + 5
            
      count -= 1
      if count > 0:
        deque.append([value, count])
      else:
        score += value
  return score


def bowling_score(frames):
    rolls = list(frames.replace(' ',''))
    for i, hit in enumerate(rolls):
        if hit == 'X':
            rolls[i] = 10
        elif hit == '/':
            rolls[i] = 10 - rolls[i - 1]
        else:
            rolls[i] = int(hit)
    score = 0
    for i in range(10):
        frame = rolls.pop(0)
        if frame == 10:
            score += frame + rolls[0] + rolls[1]    # Strike!
        else:
            frame += rolls.pop(0)
            score += frame
            if frame == 10:
                score += rolls[0]                   # Spare!
    return score