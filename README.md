# agricola.tools
Tools for playing Agricola on BGA

The purpose of the project is to analyze realtime public information about board game [agricola](https://boardgamegeek.com/boardgame/200680/agricola-revised-edition). Speaking specific, the project is able to show the card rank that have been played on the player board on the website [BoardGameArena(BGA)](https://boardgamearena.com). The card rank [statistic](https://boardgamearena.com/forum/viewtopic.php?t=31498) is also from the website.


In the future, we hope to develop tools with more functions that help new players get familiar and better with the game faster. Also, we hope to deploy the tool into various platform such as windows, ubuntu, M1 mac, etc.

# Contents
- [agricola.tools](#agricolatools)
- [Contents](#contents)
- [Installation](#installation)
- [Feature](#feature)
- [CheckList](#checklist)

# Installation
## Download
```bash
$git clone https://github.com/JiaYouChen2003/agricola.tools.git
```

## Build Environment
```bash
$conda create -n ENV_NAME python=3.9
$conda activate ENV_NAME
$pip install -r requirements.txt
```

## How to run the project
```bash
$conda python main.py
```

# Feature
<div align="center">
<img src="https://github.com/JiaYouChen2003/agricola.tools/blob/main/raw_asset/layout.png" width="81%" height="81%">
</div>

# CheckList
## Big
1. scrape data for draft phase (require login)
2. give more information to user (ex: average ranking of card seen, tips for playing specific card)

## Small
1. change const_agricola.py to json