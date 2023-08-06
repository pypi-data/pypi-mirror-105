# python-library-mockup
Template repository to create a python library (like julearn)


## Instructions

1. Create a repository on Github using this one as a template.
2. Clone your repository.
3. Change the name of the library (currently `mockup`)
4. Replace the following tokens with search and replace.

| Token  | Content | Example |
| ------------- | ------------- |------------- |
| `brainrevenge`  | Package name  | `julearn` |
| `https://github.com/brainrevenge/brainrevenge` | Github URL   | `https://github.com/juaml/julearn/` |
| `https://brainrevenge.github.io/brainrevenge/` | DOCs URL   | `https://juaml.github.io/julearn` |
| `Fede Raimondo` | Author's name | `Fede Raimondo` |
| `f.raimondo@fz-juelich.de` | Author's name | `f.raimondo@fz-juelich.de` |
| `BrainRevenge Project Library` | Short description | `FZJ AML Library`

4. Go to https://pypi.org/
   1. login (maybe create an account)
   2. Go to account settings
   3. Scroll down to API tokens
   4. Create a token for all projects, take note.
5. Repeat 4. but for https://test.pypi.org
6. On your Github repository, go to "Settings" and the "Secrets". Add the respective `PYPI_TOKEN` and `TESTPYPI_TOKEN`
7. Commit the changes and push to your repository.
8. Open the documentation and follow the instructions to release a version.