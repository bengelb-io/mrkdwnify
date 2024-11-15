# mrkdwnify

mrkdwnify is an adaptation of the javascript html-to-mrkdwn library.
There are some small implementation differences between html-to-mrkdwn and mrkdwnify.

If you don't know what mrkdwn is, it's a subset of Markdown made by Slack, to enable users to craft nicely formatted messages on their platform.
Do not use this if you're looking for a regular html to markdown parser. Try: https://github.com/matthewwithanm/python-markdownify

`mrkdwnify` itself is derived directly from the python-markdownify library.
It overrides several methods from the original library and passes option presets to make outputs compatible with the mrkdwn spec.

1. Consecutive <a> and <img> are not treated as inline elements.
2. For "checked" attributes in input tags you need to provide a "true" value

Ex:
```<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" checked="true">item</li>``` => ☑︎ item

Other than that the implementation should be the same.

Important things to note:
- ```<table>``` elements will not be rendered at all (not even their content) unless you pass `render_tables=True` as a keyword argument.

# Installation 
Until I can figure out PyPi:
```bash
pip install git+https://github.com/bengelb-io/py-html-to-mrkdwn
```

# Use

```python
from mrkdwnify import mrkdwnify

html = "<h1>Hello this is a mrkdwn header!</h1>"
mrkdwn = mrkdwnify(html) # *Hello this is a mrkdwn header!*

html = '<p>Hello this is an inline link! <a href="https://www.example.com">Example</a></p>'
mrkdwn = mrkdwnify(html) # Hello this is an inline link! <https://www.example.com|Example>
```