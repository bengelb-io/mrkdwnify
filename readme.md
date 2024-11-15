# mrkdwnify

mrkdwnify is an adaptation of the javascript html-to-mrkdwn library, that uses the markdownify (as html-to-mrkdwn uses TurnDown) as its base.
There are some small implementation differences between html-to-mrkdwn and mrkdwnify.

1. Consecutive <a> and <img> are not treated as inline elements.
2. For "checked" attributes in input tags you need to provide a "true" value:
Ex: '<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" checked="true">item</li>' => ☑︎ item

Other than that the implementation should be the same.

Other important things to note:
- <table> elements will not be rendered at all unless you pass `render_tables=True` as a keyword argument.
- Mrkdwn is a subset of Markdown so there aren't alternative options

# Installation 
### (till I can figure out PyPi)

```bash
pip install git+https://github.com/bengelb-io/py-html-to-mrkdwn
```

# Use

```python
from mrkdwn import mrkdwnify

html = "<h1>Hello this is a mrkdwn header!</h1>"
mrkdwn = mrkdwnify(header) # *Hello this is a mrkdwn header!*

html = '<p>Hello this is an inline link! <a href="https://www.example.com">Example</a></p>'
mrkdwn = mrkdwnify(header) # Hello this is an inline link! <https://www.example.com|Example>
```