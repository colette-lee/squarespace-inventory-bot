# squarespace-inventory-bot
Automates data input into SquareSpace's online platform

Uses Python3 and Selenium webdriver
Use pip3 to install selenium and webdriver-manager to use script

Takes an input text file in this format:
model-number,retail-price,name,size,size,size

See test files for examples.

Run with command:
`python3 inventory_bot.py name-of-text-file.txt`
or
`python3 inventory_bot.py name-of-text-file.txt test` to run under test sizes

Note: code is writeten specific to client's SquareSpace Page

