# flyonthewall

<b>Parse 4chan boards and filter posts with relevant keywords</b>

Must include keyword file in root directory: keywords.txt

<b>keyword.txt format:</b>
 - One keyword per line
 - If keyword has similar words to exclude, use comma-separated list separated from keyword by '|'  character

<b>Example keywords.txt:</b>

stellar

lumens

str|strong,strength,stress,stretch,strap,straw,strangle

xlm

In above example, these words will be included in search:
- stellar
- lumens
- str
- xlm

And these words will be excluded from search:
- strong
- strength
- stress
- stretch
- strap
- straw
- strangle
