import re


class IntentContainer:
    def __init__(self):
        self.intent_lines, self.entity_lines = {}, {}
        self.intents, self.entities = {}, {}
        self.must_compile = True
        self.i = 0

    def add_intent(self, name, lines):
        self.must_compile = True
        self.intent_lines[name] = lines

    def remove_intent(self, name):
        self.must_compile = True
        if name in self.intent_lines:
            del self.intent_lines[name]

    def add_entity(self, name, lines):
        self.must_compile = True
        self.entity_lines[name] = lines

    def remove_entity(self, name):
        self.must_compile = True
        if name in self.entity_lines:
            del self.entity_lines[name]

    def _create_pattern(self, line):
        for pat, rep in (
                (r'\(([^\|)]*)\)', r'{~(\1)~}'),
                (re.escape, None),
                (r'\\ ', r' '),
                (r'(?<!\\{\\~)\\\(', r'('),
                (r'\\\)(?!\\~\\})', r')'),
                (r'\\{\\~\\\(', r'\\('),
                (r'\\\)\\~\\}', r'\\)'),
                (r'\\\|', r'|'),
                (r'\\{', '{'),
                (r'\\}', '}'),
                (r'(\w)([^\w\s}])', r'\1 \2'),
                (r'([^\w\s{])(\w)', r'\1 \2'),
                (r' {} '.format, None),
                (r'(\\[^\w ])', r'\1?'),
                (r'(?<=\w)(\\\s|\s)+(?=\w)', r'\\W+'),
                (r'\s+', r'\\W*')
        ):
            if callable(pat):
                line = pat(line)
            else:
                line = re.sub(pat, rep, line)
        return line

    def _create_intent_pattern(self, line):
        line = self._create_pattern(line)
        replacements = {}
        for ent_name in set(re.findall(r'{([a-z_]+)}', line)):
            replacements[ent_name] = r'(?P<{}__{{}}>.*)'.format(ent_name)
        for ent_name, ent in self.entities.items():
            replacements[ent_name] = r'(?P<{}__{{}}>{})'.format(ent_name, ent)
        for key, value in replacements.items():
            line = line.replace('{' + key + '}', value.format(self.i), 1)
            self.i += 1
        return line

    def create_regex(self, lines):
        return r'({})'.format('|'.join(
            self._create_intent_pattern(line) for line in sorted(lines, key=len, reverse=True)
        ))

    def compile(self):
        self.entities = {
            ent_name: r'({})'.format('|'.join(
                self._create_pattern(line) for line in lines
            ))
            for ent_name, lines in self.entity_lines.items()
        }
        self.intents = {
            intent_name: re.compile(self.create_regex(lines), re.IGNORECASE)
            for intent_name, lines in self.intent_lines.items()
        }
        self.must_compile = False

    def calc_intents(self, query):
        if self.must_compile:
            self.compile()
        for intent_name, intent in self.intents.items():
            match = intent.match(query)
            if match:
                yield {'name': intent_name, 'entities': {
                    k.rsplit('__', 1)[0]: v for k, v in match.groupdict().items() if v
                }}

    def calc_intent(self, query):
        return min(
            self.calc_intents(query),
            key=lambda x: sum(map(len, x['entities'].values())),
            default={'name': None, 'entities': {}}
        )
