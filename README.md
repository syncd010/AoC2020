# [Advent of Code 2020](https://adventofcode.com/2020) in Python

This year i was a bit lazy, and went straight to Python. To compensate for that i'll try do document the code a little bit better than in previous years, and write some generic impressions about each day here.

Python version is 3.9, and it probably won't work with earlier versions, particularly because the `typing` module is used extensively. No other external modules will be used, not even `numpy`.

All code is on `./aoc`, my input files as well as test inputs are in `./res`.

## Post-event impressions
This was a fun Advent of Code. I feel that it was easier than last year's, where from the middle on it seemed that every 2 days was a demanding problem. This year, apart from day 20 which was genuinely demanding (it felt like several days compressed into one, but it was fun), and day 23, in which i stumbled because my mental model wasn't the most appropriate, the other's difficulty curve was well calibrated.

## Usage
To run:
> python aoc/aoc.py [-f FILE] [-t] day

This will run the 2 parts of the specified `day` using `FILE` as input. If no file is specified `./res/input{day}` is used as input. If no file is specified and `-t` is used, `./res/input{day}Test` is used instead. 

---

## [Day 1](https://adventofcode.com/2020/day/1)
Just a simple warm up.

## [Day 2](https://adventofcode.com/2020/day/2)
Still warming up.

## [Day 3](https://adventofcode.com/2020/day/3)
The `count_colisions` function does all the work, and its comment is explicit:
    Traverse area_map, starting from (0,0) with step (down, right), counting the positions that are marked with #
Traverse here means reaching the bottom. Just need to make sure to take the width modulus when calculating the column to access.

## [Day 4](https://adventofcode.com/2020/day/4)
After converting the input to a `List` of `Dicts` where each one has the attributes of a passport, the answers are simple

## [Day 5](https://adventofcode.com/2020/day/5)
Recognize that the input is given in binary for the row and column and the answer is straightforward.

## [Day 6](https://adventofcode.com/2020/day/6)
`Sets` do all the work here. Just collect all the questions for an answer in a set with union for part 1 and intersection for part 2.

## [Day 7](https://adventofcode.com/2020/day/7)
A bit more work on this one, mainly because the input needs to be converted to a suitable form. The plan is to convert it into a dictionary with one entry for each rule, each entry with the list of the respective bags, represented as a tuple of *quantity*, *bag type*.

Part 1 asks in how many rules can a specific bag be on its contents, so we the strategy is:
1. *invert* the dictionary: for each possible bag, collect all the bags where that bag is in the contents and put them in the bag's content in the inverted dictionary.
2. traverse (depth-first) the inverted dictionary starting from the desired bag (`shiny gold`) and collecting all the unique bags we visit.

Part 2 is somewhat simpler, as we use the original dictionary constructed from the input. Like in the previous part, traverse it collecting the bags, and just making sure that we also collect and take into account the `quantity` of each element.

## [Day 8](https://adventofcode.com/2020/day/8)
So we get to our first interpreted puzzle. If this is anything like the last year, it will be the first of many, so it would probably be a good idea to give some structure to this solution, given that it will probably be reused and extended later. Nevertheless i got the impression that the problem's description was too vague to be able to properly structure any future extended interpreter, so i didn't do this right away.

There's an `Instruction` with its `operation` and `argument` and a `Console` that executes a single instruction, keeping track of its instruction pointer and an accumulator.

Part 1 keeps track of which instructions are executed until there's a repeat and returns the accumulator result. Part 2 reverses `nop` with `jmp` and vice-versa, executing each resulting program and checking if the program's end was reached.

## [Day 9](https://adventofcode.com/2020/day/9)
Nothing notable here, brute-force check whether 2 numbers add up to a given one (in part one) and brute-force find contiguous numbers that add up to a given one (in parte two).

## [Day 10](https://adventofcode.com/2020/day/10)
The first puzzle that gives me pause appears. 

Part 1 was simple enough - take a diff of the input list and count the 1 and 3 differences.

Part 2 was very instructive because i didn't grab it by the easier and obvious angle. My first thought was calculating the number of *branches* possible in each step, and from that construct a solution, so i went with that and reached a solution, but it leads to a non-obvious and needlessly complex algorithm. On a high-level, for each step i calculated the number of possible branches (by checking how many of the difference between the next 3 elements are <= 3) and afterwards traverse that list, and for each element `n` (which is the branching factor on that element) increase the next `n` elements by the number of paths that have reached element `n`.

After looking at the daily solution thread on reddit the easier and more obvious solution become clear: the number of paths that can reach an element n is the sum of the of paths that reach n-1, n-2 and n-3. The easiest way to do this is to use a list of all the reachable values, where the index is the value and the content is the number of paths that lead to that element. Start with 1 on the 0th element and 0 on every other and for each one sum the values of the previous 3. Conceptually much clearer and simple. 

I nevertheless kept the old code commented out to serve as a lesson to not blindly follow a solution just because it works.

## [Day 11](https://adventofcode.com/2020/day/11)
The first of the cellular automata. There's a bit of code, but it's nothing much. The only thing that might need explaining is that i decided to envelop the board in a frame of *empty* so that i don't have to check whether indices are valid at every step (`>=0`, `<len`).

## [Day 12](https://adventofcode.com/2020/day/12)
For this i created a `Position` class, with arithmetic operators defined. This whole puzzle could be directly done using imaginary numbers, and it would be simpler given that the rotation was simply a matter of multiplying by 0-1j, but i chose to use an explicit Position class to make it somewhat more clear.

## [Day 13](https://adventofcode.com/2020/day/13)
The first part was direct: find the minimum multiple of the numbers greater than `min_time`.

For the second part i noticed the warning in the problem's description, that a brute-force approach wouldn't cut it, and looked for a closed-form solution. After some thought i become convinced that some high-level number theory knowledge was needed to solve it, which i didn't have, become lazy and just looked in reddit for clues, which led me to the *Chinese Remainder Theorem* on Wikipedia. So in the end, no specialized number theory knowledge was needed, and a brute-force approach was used, just not a naive one.

## [Day 14](https://adventofcode.com/2020/day/14)
Bitwise operations, none too hard but confusing enough to take some time.

In part 1 the strategy is to create 2 masks, mask1 with X's replaced by 1 and mask2 with X'2 replaced by 0, then do (arg & mask1) | mask2, which is:
1. (arg & mask1) | mask2 = arg where mask had X's ((arg & 1) | 0 = arg)
2. (arg & mask1) | mask2 = mask where mask didn't have X's ((arg & m) | m = m)

In part 2, it's a partial bitwise or between the mask and the address (which is done manually), and then "unravel" the resulting mask by substituting all X's by 0 and 1, which is done in the recursive function.

## [Day 15](https://adventofcode.com/2020/day/15)
[Van Eck's Sequence](https://oeis.org/A181391)
First approach was brute force, computing all elements and searching through them to get the last position seen. This would obviously not work on the second part, so i took the usual path of using a dictionary, which stores the last time the element was seen. Some care is needed with the indices.

## [Day 16](https://adventofcode.com/2020/day/16)
This was a fun one, though it takes some work. Using pythons `range` to represent the intervals, being able to check if a number is in the range (`in`), with lots of list comprehensions and abusing the functions `all` and `any` does the trick.

Part 1 collects all ticket numbers that aren't in any of the ranges of the fields. In python this reads almost literally.

Part 2 is:
- Collect valid tickets: tickets that have all their numbers in at least one of the field's ranges
- For each field collect which positions are possible for it. A position is possible for a field if all ticket values in that position are in at least one of the ranges for the field.
- Assume that there's at least one field that can be in only one position, and do a basic constraint propagation, removing that position from the other fields possible positions and repeating the process.
- Assuming that the previous step resulted in unique positions for each field, get our ticket positions for the keys that start with "departure".

## [Day 17](https://adventofcode.com/2020/day/17)
A cellular automata in an infinite grid and in 3D with simple rules. Part 1 seemed simple enough, but it was to be expected that performance would be the critical issue in part 2, either by increasing the number of epochs or something else - evolving the grid to 4D was a smart twist.

Nevertheless, not knowing what to expect in part 2, i proceeded by just making sure that i used a representation that would allow possible improvements in the future. So, instead of representing the full board in a multi-dimensional array, i chose to use only the active positions in a list. On each epoch determine the boundaries of the active positions, add +2 on each dimension to account for the possible growing of the board, and iterate on each of the possible positions, as determined by those boundaries. For each position count all active positions that are within distance 1 (on all dimensions), making sure to subtract 1 if the position is active as it was also counted, and apply the cellular automata rules, creating a new list of active positions for the next epoch.

Adapting the algorithm for part 2 (in 4D), was simple, as it only needed to account for one more dimension, but performance suffered as expected (first run took 160s). With some optimizations, the main one being filtering the active positions on each dimension iteration to only consider those that are within distance 1 on that dimension's value (which in hindsight should have been done on the first try), the runtime come down to < 1s.

## [Day 18](https://adventofcode.com/2020/day/18)
Evaluating an expression in infix notation without operator priorities or with the priorities changed in part 2. The correct way to do it would be to change it to RPN and evaluate it, but given that part 1 asked for the evaluation without priorities (except for `(` and `)`) i thought that directly evaluating the expression would work.

The solution is in `eval_infix`, which evaluates the infix expression sequentially. It treats the input as a stack, poping the 3 args for each expression, recursively calling itself if a `(` is encountered, applying the respective operator and pushing the result back into the stack. It consumes the input as it goes along, and expects it to be passed in reversed order, so that it can be used as a stack directly.

Ugly but it works. 

For part 2, and given that `eval_infix` already considers priorities around parentheses, the strategy is to add them around all the `+` operators in the input before evaluating the expression. There's the added complication that either of the 2 args can be an expression surrounded by parentheses, whose boundaries must be found, but it works.

In retrospective i think that converting the input to RPN would be a better and cleaner strategy, given that the resulting algorithm wouldn't be more complex, and would be cleaner and more general (infix to RPN using (Shunting-yard algorithm)[https://en.wikipedia.org/wiki/Shunting-yard_algorithm], eval would be trivial).

## [Day 19](https://adventofcode.com/2020/day/19)
Reading a grammar and parsing a list of strings according to that grammar. After converting the grammar rules to a dictionary, the matching of a string is done recursively in `match`. This function returns how many characters from the given string are matched, starting at a given rule. More than one value can be returned, because of alternative sub-rules. If no match if possible the empty list is returned, if all the string was matched, its length should be returned.

This approach worked for part 1 and 2 without modification, so the warning/tips on part 2 didn't apply. Guess that warning would be relevant if part 1 was solved with regular expressions (transforming the grammar to a regexp and then directly applying it to the messages).

## [Day 20](https://adventofcode.com/2020/day/20)
It's Sunday, so i guess the goal is to make us spend the whole day solving this puzzle. It's a fun and interesting one nevertheless.

Some notes regarding the solution:
- `Tile` represents a tile, with its key and image. The image edges are treated specially to facilitate posterior manipulations: they are represented as integers after converting each each to binary, and are stored in the `edges` member. The function `edges_reversed` returns these edges with the bits reversed, like what an edge would become after being flipped.
- The `is_compatible` function returns the sequence of operations to make a tile compatible with certain left and top edges, if any.
- For part 1, to discover corner tiles, a sufficient condition for a tile to be in the corner is for it to have 2 edges which aren't compatible with any of the others (either straight or reversed). This isn't a necessary condition, but it's sufficient, so i just took a chance and the format of the input works with this approach.
- For part 2, there's no shortcut, the full image must be constructed. This is done by Depth-First-Search, trying to place tiles on the puzzle left-to-right and top-to-bottom, in a compatible way, storing the operations that are needed to make a tile compatible along the way. If a solution to the puzzle is found, the rest is just some straightforward manipulations: remove borders, join images, and do a convolution with a mask.

Nice one, but a lot of work. It amazes me how people were able to solve this in < 1 hour...

## [Day 21](https://adventofcode.com/2020/day/21)
After yesterday this was an easy one. Using `sets` to keep the lists of ingredients and alergens do most of the work. Somehow, i found that manipulating the structures i created was a bit cumbersome (Dicts with Sets), so there should be some more straightforward solution, but this was what come out on the first try.

## [Day 22](https://adventofcode.com/2020/day/22)
Yet another simple card game. Just 2 notes: 1) using a list for each hand and poping from the front is a bit inefficient, but the problem is small, so it works; 2) the hash function used to check if the hands have been seen before is very simple, and works because the input is a list of unrepeated numbers.

## [Day 23](https://adventofcode.com/2020/day/23)
This one stumped me for a long time. Part 1 is just some list manipulations, sloppily done because neither performance nor space are an issue.

For part 2, the brute-force approach of part 1 wasn't going to cut it. Even optimizing the hell out of it, considering the number of iterations m and the number of elements n, any brute-force solution similar to part 1 would by O(mn) because for each iteration we are searching for an element on the (unsorted) list and moving elements there which is O(n) (the expected value of ops is n/2 for the searching and moving). Anything O(mn) with m = 10M, n = 1M in Python isn't good news. I tried to look for some structure or order on the manipulations that would enable some prediction in future iterations but couldn't find one, and probably with good reason: the order of the first manipulations depend on the order of elements on the input list, and that has an effect on subsequent manipulations, so it can't be predicted irrespective of the input. Likewise hoping that there are "loops" in the manipulations and using a strategy of memoization of seen positions isn't feasible because of the size (1M ints) of the problem.

So, the only solution i saw was brute-force, but the approach of part 1 wasn't feasible, and i got stuck a long time. I guess it was a case of "if all you have is a hammer, everything looks like a nail", the hammer in this case being Python's lists, which are really arrays and have been (ab)used for the previous 23 days. In the end i remembered about proper lists, C lists, with pointers and such, and the solution become clear. The manipulations are trivial considering the elements as nodes in a double linked list with pointers, and that's what was implemented. Now, of course this is not pythonic, but i let it stay because i think it fits the solution better and it was clearer to me. It could have been implemented with arrays, with the index representing the element, the value being the index of the next element and the previous being just idx-1, but that's not the mental model i have about the problem so i didn't go with it.

Stuck for a long time, but it was another day in which i learned (or remembered) something.

## [Day 24](https://adventofcode.com/2020/day/24)
Guess we're getting to the home stretch, so this was an easy one. Of note: 1) the board is represented as a list of `Positions` (actually a `set` for performance reasons, as there some membership checking operations in part 2) and 2) the way moves affect positions on the board are: 'e', 'w' (+- 2, 0) on the x-axis, others: (+-1,+-1) on the x and y-axis, therefore allowing the identification of hexagonal tiles in 2D. 

Part 2 isn't optimized at all and is somewhat slow, but the code is straightforward and clear IMO.

## [Day 25](https://adventofcode.com/2020/day/25)
And that's a wrap with a lesson in cryptography safety. Until next year.