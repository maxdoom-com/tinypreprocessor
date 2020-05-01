import tempfile, os

class ConditionStack:
    def __init__(self):
        self._bools = []

    def push(self, value):
        self._bools.append(value)

    @property
    def is_true(self):
        return self._bools[-1]

    def pop(self):
        self._bools = self._bools[0:-1]


class TinyPreProcessor:
    def __init__(self, suffix=None):
        self._tmpfile = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)
        self._conditions = ConditionStack()
        self._conditions.push(True)
        self._defined = set()

    def __del__(self):
        os.unlink(self._tmpfile.name)

    def load(self, filename):
        src = open(filename, 'rt')
        for line in src:
            if line.startswith('#'):
                directive, argument = self._parse(line)

                if directive == 'define':
                    self._defined.add(argument)

                elif directive == 'undef':
                    self._defined.remove(argument)

                elif directive == 'ifdef':
                    self._conditions.push(argument in self._defined)

                elif directive == 'ifndef':
                    self._conditions.push(not argument in self._defined)

                elif directive == 'endif':
                    self._conditions.pop()

                elif directive == 'include':
                    if self._conditions.is_true:
                        self.load(argument)

                else:
                    if self._conditions.is_true:
                        self._tmpfile.write(line.encode())

            else:
                if self._conditions.is_true:
                    self._tmpfile.write(line.encode())


    def done(self):
        self._tmpfile.close()
        return self._tmpfile.name

    def _parse(self, line):
        line = line.rstrip()

        if line.startswith('#'):
            line = line[1:]

        fields = [ part for part in line.split(' ') if part != '' ]

        if len(fields) == 2:
            return fields[0], fields[1]
        elif len(fields) == 1:
            return fields[0], None
        else:
            return None, None


if __name__ == '__main__':
    import sys
    pp = TinyPreProcessor()
    pp.load(sys.argv[1])
    tmp_file_name = pp.done()
    # the temp file will be deleted together with the preprocessor!
