from padaos import IntentContainer


class TestIntentContainer:
    def setup(self):
        self.container = IntentContainer()

    def test(self):
        self.container.add_intent('hello', [
            'hello', 'hi', 'how are you', "what's up"
        ])
        self.container.add_intent('buy', [
            'buy {item}', 'purchase {item}', 'get {item}', 'get {item} for me'
        ])
        self.container.add_entity('item', [
            'milk', 'cheese'
        ])
        self.container.add_intent('drive', [
            'drive me to {place}', 'take me to {place}', 'navigate to {place}'
        ])
        self.container.add_intent('eat', [
            'eat {fruit}', 'eat some {fruit}', 'munch on (some|) {fruit}'
        ])
        self.container.compile()
        assert self.container.calc_intent('hello')['name'] == 'hello'
        assert not self.container.calc_intent('bye')['name']
        assert self.container.calc_intent('buy milk') == {
            'name': 'buy', 'entities': {'item': 'milk'}
        }
        assert self.container.calc_intent('eat some bananas') == {
            'name': 'eat', 'entities': {'fruit': 'bananas'}
        }
