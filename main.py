import random
import tkinter as tk

class TypingSpeedTest:
    def __init__(self, master):
        self.master = master
        self.master.title('typingspeedtest')  # Set the window title
        self.master.geometry('1920x1080')  # Set the window size
        self.master.configure(bg='#f0f0f0')  # Set the background color

        # Set the font for text and buttons
        self.master.option_add("*Label.Font", "consolas 30")
        self.master.option_add("*Button.Font", "consolas 30")

        self.words_list = self.load_words_from_file('words.txt')
        self.textToType = self.generatePhrase()
        self.splitIndex = 0  # Track the position in the sentence
        self.timePassed = 0  # Track the time passed
        self.writing = True
        self.mistakes = []  # Track mistakes made by the user

        # Set up the user interface
        self.UIsetup()

        self.master.after(60000, self.endTest)  # End test after 60 seconds
        self.master.after(1000, self.updateTimer)  # Update timer every second

    def load_words_from_file(self, filename):
        """
        Load words from a specified file and return them as a list

        Parameters
        ----------
        filename(str) : The name of the file containing words.

        Returns
        -------
        list: A list of words.
        """
        with open(filename, 'r', encoding='utf-8') as file:
            words = file.read().splitlines()
        return words

    def generatePhrase(self, word_count=50):
        """
        Generate a random phrase with a specified number of words

        Parameters
        ----------
        word_count(int) :The number of words to include in the phrase

        Returns
        -------
        final_phrase(str) : A generated phrase containing random words
        """
        phrase = []
        punctuation = ['.', '?', '!']
        small_punctuation = [',', ';']
        list_punctuation = punctuation + small_punctuation

        word_counter = 0  # Counter for punctuation
        sentence_counter = 0  # Counter for punctuation
        capitalize_next = False  # Flag to determine if the next word should be capitalized

        for i in range(word_count):
            word = random.choice(self.words_list)

            # Capitalize the word
            if i == 0 or capitalize_next:
                word = word.capitalize()
                capitalize_next = False

            phrase.append(word)

            word_counter += 1
            sentence_counter += 1

            # Insert commas and semicolons every 5-9 words
            if word_counter >= random.randint(5, 9):
                phrase.append(random.choice(small_punctuation))
                word_counter = 0  # Reset the word counter after adding punctuation

            # Insert punctuation every 10-15 words
            if sentence_counter >= random.randint(10, 15):
                phrase.append(random.choice(punctuation))
                capitalize_next = True  # Set the flag to capitalize the next word
                sentence_counter = 0

        # Remove spaces before punctuation
        final_phrase = ' '.join(phrase)
        for punctuations in list_punctuation:
            final_phrase = final_phrase.replace(f' {punctuations}', punctuations)

        return final_phrase


    def UIsetup(self):
        """
        Create the user interface components for the typing test

        Returns
        -------
        None
        """
        # Label for text that has been typed
        self.textWritten = tk.Label(self.master, text='', fg='grey')
        self.textWritten.place(relx=0.5, rely=0.5, anchor='e')  # Position on the right

        # Label for the remaining text to type
        self.textRemaining = tk.Label(self.master, text=self.textToType, bg='#f0f0f0')
        self.textRemaining.place(relx=0.5, rely=0.5, anchor='w')  # Position on the left

        # Label for the current character to type
        self.currentChar = tk.Label(self.master, text=self.textToType[self.splitIndex], fg='grey')
        self.currentChar.place(relx=0.5, rely=0.6, anchor='n')  # Position above the others

        # Label for the timer
        self.timerText = tk.Label(self.master, text='0 Seconds', fg='grey')
        self.timerText.place(relx=0.5, rely=0.4, anchor='s')  # Position below the others

        # Bind the key press event to handle typing
        self.master.bind('<Key>', self.handleKeypressEvent)

    def handleKeypressEvent(self, event=None):
        """
        Handle the key press event to check what the user typed

        Parameters
        ----------
        event: Keyboard event

        Returns
        -------
        None
        """
        if self.writing:
            expected_char = self.textRemaining.cget('text')[0]  # Get the expected character
            typed_char = event.char  # Get the character that the user typed

            # Check if the typed character matches the expected character
            if typed_char == expected_char:
                self.updateLabel(typed_char)  # Update text if correct
            else:
                self.highlightError(expected_char)  # Highlight the expected character if wrong
                self.mistakes.append(typed_char)  # Store the mistake

    def updateLabel(self, typed_char):
        """
        Update text when the user types the correct character

        Parameters
        ----------
        typed_char (str): The character the user typed

        Returns
        -------
        None
        """
        # Update the remaining text and the written text
        self.textRemaining.configure(text=self.textRemaining.cget('text')[1:])  # Remove the typed character
        self.textWritten.configure(text=self.textWritten.cget('text') + typed_char)  # Add to the typed text

        if self.textRemaining.cget('text'):  # Check if there are remaining characters
            self.currentChar.configure(text=self.textRemaining.cget('text')[0], fg='grey')  # Show the next character
        else:
            self.endTest()  # End the test if no characters remain

    def highlightError(self, expected_char):
        """
        Highlight the expected character in red if the wrong key is pressed

        Parameters
        ----------
        expected_char (str): The expected character to continue typing

        Returns
        -------
        None
        """
        self.currentChar.configure(text=expected_char, fg='red')  # Change color to red to show error

    def updateTimer(self):
        """
        Update the timer label every second.

        Returns
        -------
        None
        """
        if self.writing:  # Check if writing is still active
            self.timePassed += 1  # Add the time passed
            self.timerText.configure(text=f'{self.timePassed} Seconds')  # Update the timer text
            self.master.after(1000, self.updateTimer)  # Call this function again after 1 second

    def endTest(self):
        """
        End the typing test and show the results.

        Returns
        -------
        None
        """
        self.writing = False  # Stop writing
        words_typed = len(self.textWritten.cget('text').split())  # Count the words typed

        # Calculate typing speed in words per minute
        time_in_minutes = self.timePassed / 60  # Convert seconds to minutes
        if time_in_minutes > 0 :
            typing_speed = (len(words_typed)/5) / time_in_minutes
        else :
            typing_speed = 0  # Avoid division by zero

        # Remove text from the screen
        self.timerText.destroy()
        self.currentChar.destroy()
        self.textRemaining.destroy()
        self.textWritten.destroy()

        # Show the results to the user
        self.result_label = tk.Label(self.master, text=f'Words per Minute: {typing_speed:.0f}', fg='grey', bg='#f0f0f0')
        self.result_label.place(relx=0.5, rely=0.4, anchor='center')  # Center the result label

        # Create a button to try again
        self.retry_button = tk.Button(self.master, text='Try Again', command=self.restartTest, bg='grey', fg='black')
        self.retry_button.place(relx=0.5, rely=0.6, anchor='center')  # Center the retry button

        # Display mistakes made by the user
        self.mistakes_label = tk.Label(self.master, text=f'Mistakes: {self.mistakes}', fg='grey', bg='#f0f0f0')
        self.mistakes_label.place(relx=0.5, rely=0.5, anchor='center')  # Center the mistakes label

    def restartTest(self):
        """
        Restart the typing game.

        Returns
        -------
        None
        """
        # Remove the result and retry button
        self.result_label.destroy()
        self.retry_button.destroy()
        self.mistakes_label.destroy()

        # Get a new sentence and reset variables
        self.textToType = self.generatePhrase()  # Generate phrase
        self.splitIndex = 0  # Reset the position in the sentence
        self.timePassed = 0  # Reset the time passed
        self.writing = True  # Allow writing again
        self.mistakes = []  # Reset mistakes

        # Set up the user interface again
        self.UIsetup()
        self.master.after(60000, self.endTest)  # Restart the timer for the test duration
        self.master.after(1000, self.updateTimer)  # Restart the timer update

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    typing_test = TypingSpeedTest(root)
    root.mainloop()
