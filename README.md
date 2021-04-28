# COMP3981_Project
COMP3981 Abalone project 

Setup:


1. If needed, install Python and Pip: https://www.python.org/
2. Install PyCharm: https://www.jetbrains.com/pycharm/
3. Install pyGame and thorPy through command line.
3a. Open command prompt and install pygame using the following commmand:
  'pip install pygame'
3b. Open command prompt and install thorPy using the following command:
  'pip install thorpy'

  Alternatively, thorPy and pyGame can be installed through PyCharm by navigating to 
  File > Settings > Project: COMP3981_Project > Python Interpreter. On the bottom left 
  of the list, click the '+' icon, search for 'pygame' and/or 'thorpy', then click 
  'Install Package'

4. In PyCharm, navigate to main.py and open the file. 
5. Run the program by one of the following methods:
  I. Click the play button on the top right of the window, above the text editor. 
  II. Click the play button next to the "if __name__ == '__main__'" statement.
  III. On the top dropdowns bar, click Run > Run 'main'.


--------------------------------------

Setup for StateSpace Generator:

In order to test input files, add the input file to the GUI folder. You can now enter the name
of the input file where "Test1.input" is written as a string. The program will automatically load and
then generate all possible board configurations for the specified input file. Board and move files will be found
in the GUI folder. 
Note: Run the board.py file directly, using main.py will not provide access to the state generator.
Note: The move file representation for each line is [[Old position], [New position], Movement_Performed]

1. Complete setup noted above. 
2. Using Pycharm, navigate to GUI > board.py, scroll to the bottom. Next to the statement "if __name__ == 'main'" and click the play button to the left of it.
