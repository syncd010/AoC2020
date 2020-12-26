#!/bin/sh

if [ -z "$1" ]
then
    echo "Please provide a day number"
    exit
fi

DAY="day$1"

if [ -f "./aoc/day$1.py" ]
then
    echo "Day $1 already exists"
else
    cp "./aoc/day_template.py" "./aoc/day$1.py"
    touch "./data/input$1"
    touch "./data/input$1Test"
    echo "Day $1 created"
fi

