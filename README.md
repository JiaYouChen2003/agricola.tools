# agricola.tools
Tools for playing Agricola on BGA

The purpose of the project is to analyze realtime public information about board game [agricola](https://boardgamegeek.com/boardgame/200680/agricola-revised-edition). Speaking specific, the project is able to show the card rank that have been played on the player board on the website [BoardGameArena(BGA)](https://boardgamearena.com). The card rank [statistic](https://boardgamearena.com/forum/viewtopic.php?t=31498) is also from the website. \
In the future, we hope to develop tools with more functions that help new players get familiar and better with the game faster. Also, we hope to deploy the tool into various platform such as windows, Ubuntu, ios, android etc.

# Contents
- [agricola.tools](#agricolatools)
- [Contents](#contents)
- [Installation](#installation)
- [Feature](#feature)
- [CheckList](#checklist)

# Installation
## Download
```bash
git clone https://github.com/JiaYouChen2003/agricola.tools.git
```

## Build Environment
```bash
conda create -n agricola.tools python=3.9
conda activate agricola.tools
pip install -r requirements.txt
```

## How to run the project
```bash
python main.py
```

# Feature

<div align="center">
<img src="https://github.com/JiaYouChen2003/agricola.tools/blob/main/raw_asset/layout.png" width="81%" height="81%">
</div>

<div align="center">
<img src="https://github.com/JiaYouChen2003/agricola.tools/blob/main/raw_asset/layout_url.png" width="81%" height="81%">
</div>

# CheckList
## Big
- [x] scrape data for draft phase -- 2024/01/05
- [ ] give more information to user (ex: tips for playing specific card)
- [ ] scrape data for replay
- [x] anonymous player data -- 2024/02/25

## Small
- [ ] change const_agricola.py to json

## Bug
- Cannot see game in progress while login
