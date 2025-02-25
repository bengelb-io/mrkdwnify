# mrkdwnify
mrkdwnify is an adaptation of the javascript [html-to-mrkdwn](https://github.com/integrations/html-to-mrkdwn) library built upon the existing [python-markdownify](https://github.com/matthewwithanm/python-markdownify) library.

# Installation 
```bash
pip install mrkdwnify
```

# Use

```python
from mrkdwnify import mrkdwnify

html = "<h1>Hello this is a mrkdwn header!</h1>"
mrkdwn = mrkdwnify(html) # *Hello this is a mrkdwn header!*

html = '<p>Hello this is an inline link! <a href="https://www.example.com">Example</a></p>'
mrkdwn = mrkdwnify(html) # Hello this is an inline link! <https://www.example.com|Example>
```

## For Tinkerers

If you don't know what mrkdwn is, it's a subset of markdown made by Slack to enable users to craft nicely formatted messages on their platform.

If you are looking for a *html -> markdown* parser see [python-markdownify](https://github.com/matthewwithanm/python-markdownify)

`mrkdwnify` itself is derived directly from the [python-markdownify](https://github.com/matthewwithanm/python-markdownify) library.

It overrides several methods from the original library and passes option presets to match the implementation of its Javascript counterpart, with the following exceptions:

1. Consecutive <a> and <img> are not treated as inline elements.
2. For "checked" attributes in input tags you need to provide a "true" value

Javascript Version:
```<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" checked >item</li>``` => ☑︎ item
Python Version: 
```<li class="task-list-item"><input class="task-list-item-checkbox" type="checkbox" checked="true">item</li>``` => ☑︎ item

Other than that the implementation should be the same.

*Important things to note*:
- ```<table>``` elements will not be rendered at all (not even their content) unless you pass `render_tables=True` as a keyword argument.
- The mrkdwnify function behaves identically to the markdownify function, you can implement or override logic the same way you would for the original library. (see [markdownify](https://github.com/matthewwithanm/python-markdownify))
