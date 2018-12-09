from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit=None,miss=None):
        if hit and miss:
            raise InvalidGuessAttempt()
            
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
    def is_hit(self):
        if self.hit:
            return True
        return False
            
    def is_miss(self):
        if self.miss:
            return True
        return False   

class GuessWord(object):
    def __init__(self, word): 
        if not word:
            raise InvalidWordException
        self.answer = word
        self.masked = '*' *len(word)
        
        
    def perform_attempt(self, letter):
        letter = letter.lower()
        if len(letter)== 0 or len(letter) >1:
            raise InvalidGuessedLetterException()
            
        if letter in self.answer.lower():
            attempt = GuessAttempt(letter, hit=True)
            self.masked = self.unveil_word(self.answer, self.masked, letter)
        else:
            attempt = GuessAttempt(letter, miss=True)
        return attempt
        

    def unveil_word(self, answer, masked, letter):
        result = ''
        for i in range(len(self.answer)):
            if letter == self.answer[i].lower():
                result+= letter
            else:
                result += self.masked[i].lower()
        return result
        
        


class HangmanGame(object):
    WORD_LIST = ['rmotr', 'python', 'awesome']
    def __init__(self, word_list = WORD_LIST, number_of_guesses = 5):
        if not word_list:
            word_list = self.WORD_LIST
        self.remaining_misses = number_of_guesses
        selected_word = self.select_random_word(word_list)
        self.word = GuessWord(selected_word)
        self.previous_guesses = []
    
    
    def guess(self,letter):
        if self.is_finished():
            raise GameFinishedException()
                
        self.previous_guesses.append(letter.lower())
        
        attempt = self.word.perform_attempt(letter)
        if attempt.is_miss():
            self.remaining_misses -=1
            if self.is_lost():
                raise GameLostException()
                
        if self.is_won():
            raise GameWonException()
            
        return attempt
    
    def is_finished(self):
        if self.is_won() or self.is_lost():
            return True
        return False
    
    def is_lost(self):
        if self.remaining_misses < 1:
            return True
        return False
    
    def is_won(self):
        if self.word.answer == self.word.masked:
            return True
        return False
        
    @classmethod 
    def select_random_word(cls,word_list):
        if word_list == []:
            raise InvalidListOfWordsException()
        return random.choice(word_list)    
        
        