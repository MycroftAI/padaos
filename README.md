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

Padaos is nothing more than a converter between a series of example sentences and
one big chunk of regex. Each intent is a single compiled regex matcher.
