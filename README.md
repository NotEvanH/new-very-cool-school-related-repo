<a id="readme-top"></a>

<br />
<div align="center">
    <h3 align="center">Computer Science Project: NYTGames Replica</h3>
    <p align="center">A two-game arcade made in Python for my Year 11 Comp-Sci Assignment.</p>
</div>

<details>
    <summary>Table of Contents</summary>
    <ol>
        <li>
            <a href="#about-the-project">About The Project</a>
            <ul>
                <li><a href="#built-with">Built With</a></li>
            </ul>
        </li>
        <li>
            <a href="#getting-started">Getting Started</a>
            <ul>
                <li><a href="#prerequisites">Prerequisites</a></li>
                <li><a href="#installation">Installation</a></li>
            </ul>
        </li>
        <li><a href="#roadmap">Roadmap</a></li>
        <li><a href="#license">License</a></li>
        <li><a href="#creator-information">Creator Information</a></li>
        <li><a href="#acknowledgments">Acknowledgments</a></li>
    </ol>
</details>

## About The Project

This project aims to replicate two of the NYT's most popular games - Wordle and Spelling Bee. More importantly, it aims to fulfil the criteria my teacher has set because I want to pass computer science. The project has to function as a simple arcade where the user can select one of two games to play and receive some semblance of a score.

Core Features:
* Display an easy-to-understand menu where the user is able to choose which game they would like to play
* Input validation
* Give the user a score based on their performance
* Storing data
* Obviously the aforementioned games

<p align="right">(<a href="#readme-top"></a>)</p>

## Built With

The assignment outline states that the project should be made with Python. However, other technologies such as SQL have been used to extend Python's capabilities. Additionally, the assignment dictates that no external Python libraries should be used.

* ![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
* ![SQL](https://img.shields.io/badge/sql-597cc2?style=for-the-badge&logo=mysql&logoColor=ffffff)

<p align="right">(<a href="#readme-top"></a>)</p>

## Getting Started

Herein lies instruction on how to set up this project locally.

### Prerequisites
None

### Installation

For my teacher: I am aware that you normally mark these projects in PyCharm. However, since PyCharm only simulates a real terminal, some functionality reliant on ANSI codes won't work in PyCharm. Therefore, I humbly request thee to assess my project with VSCode.

1. Clone the repo
```sh
git clone https://github.com/NotEvanH/new-very-cool-school-related-repo.git
```

2. Change directory to the newly cloned repository
```sh
cd new-very-cool-school-related-repo
```

3. Run main.py with Python
e.g.
```sh
python main.py
```

<p align="right">(<a href="#readme-top"></a>)</p>

## Roadmap

- [X] Implement a basic menu for users to interact with
- [X] Recreate Wordle and Spelling Bee
- [X] Effectively store user's scores locally and display them visually at the user's request
- [X] Create a simple version of WordleBot to allow user's to assess their gameplay in comparison to the bot's
- [X] Allow users to create custom Wordle games with their own words
- [X] Make a cool - albeit completely ornamental - loading screen
- [ ] Multi-language support
    - [ ] German
    - [ ] Italian
- [X] Wordle Hints
- [ ] Spelling Bee Letters Reshuffle

## Creator Information
Made by Evan Ho

## Acknowledgments

Here are some resources that I have found useful in the creation of this project.

* [ANSI Colour Codes Cheatsheet](https://gist.github.com/JBlond/2fea43a3049b38287e5e9cefc87b2124)
* [Wordle Valid Words List](https://gist.github.com/dracos/dd0668f281e685bad51479e5acaadb93)
* [The NYTGames](https://www.nytimes.com/crosswords)