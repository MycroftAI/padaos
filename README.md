# Padaos

*A rigid, lightweight, dead-simple intent parser*

To deploy an intent parser into production with an automated feedback loop,
it's essential that the new data doesn't interfere with the old data. It's
also necessary that the parser can learn from sentences that closely match
written English (or any other language). That's what Padaos does.

## Example

```python
from padaos import IntentContainer

container = IntentContainer()
container.add_intent('hello', [
    'hello', 'hi', 'how are you', "what's up"
])
container.add_intent('buy', [
    'buy {item}', 'purchase {item}', 'get {item}', 'get {item} for me'
])
container.add_intent('search', [
    'search for {query} on {engine}', 'using {engine} (search|look) for {query}',
    'find {query} (with|using) {engine}'
])
container.add_entity('engine', ['abc', 'xyz'])
container.calc_intent('find cats using xyz')
# {'name': 'search', 'entities': {'query': 'cats', 'engine': 'xyz'}}
```

## How it works

Padaos converts a series of example sentences into
one big chunk of regex. Each intent is a single compiled regex matcher.
Here's a fex examples of the input example and the output regex.

```
This is a test
->
\W*This\W+is\W+a\W+test\W*
```

```
Eat an (apple|orange).
->
\W*Eat\W+an\W*(\W*apple\W*|\W*orange\W*)\.?\W*
```

```
Hello!
Hi!
->
(\W*Hello\W*\!?\W*|\W*Hi\W*\!?\W*)
```

```
This is something (inside parentheses)
->
(\W*This\W+is\W+something\W*\(?\W*inside\W+parentheses\W*\)?\W*)
```
