#!/usr/bin/python

import os, sys
from optparse import OptionParser

try:
    from lxml import etree
    from lxml.html.clean import Cleaner
except ImportError:
    print "Please install lxml first."
    print "http://pypi.python.org/pypi/lxml"
    exit(1)

from StringIO import StringIO

class Html2Less(object):
    """Parse HTML to extract empty CSS rulesets."""

    def __init__(self):
        self.prog = os.path.basename(sys.argv[0])

        parser = OptionParser(version="%prog 0.1", usage="%prog [options] [input files]\n" \
            "This program will read from stdin if no input files are specified.")
        parser.add_option("-d", "--delimiter", dest="delimiter", default='spaces',
            help="Delimiter: tabs or spaces? Default: spaces")
        parser.add_option("-c", "--clean", action="store_true", dest="clean_mode", default=False,
            help="Give me clean rulesets (no comments)")

        (self.options, self.args) = parser.parse_args()

        if self.options.delimiter and self.options.delimiter not in ['tabs', 'spaces']:
            parser.error("Accepted delimiter value: 'tabs' or 'spaces'")

    def identify_ruleset(self, elem):
        """Identify a ruleset - give precedence to: A) id, B) class, C) tag name."""

        identifier = elem.attrib.get('id')
        if identifier:
            identifier = "#" + identifier
        else:
            identifier = elem.attrib.get('class')
            if identifier:
                identifier = "." + identifier.split()[0]
            else:
                identifier = elem.tag

        return identifier

    def parse(self, content):
        """Clean and parse HTML content."""

        cleaner = Cleaner(style=True, links=False, page_structure=False, meta=True,
            safe_attrs_only=False, remove_unknown_tags=False)
        clean_content = cleaner.clean_html(content)

        html = etree.iterparse(StringIO(clean_content), events=("start", "end"))
        level = -1
        css = ''

        # We do not want to style these elements.
        ignore_tags = ['html', 'body', 'head', 'meta', 'title', 'script']

        if self.options.delimiter == 'spaces':
            delimiter = '  '
        else:
            delimiter = '\t'

        for action, elem in html:
            if (action == 'start'):
                identifier = self.identify_ruleset(elem)

                if elem.tag not in ignore_tags:
                    level += 1
                    css += delimiter * level + identifier + ' {\n'
                    if not self.options.clean_mode:
                        css += delimiter + delimiter * level + '/* enter your CSS here... */\n'
            else:
                if elem.tag not in ignore_tags:
                    css += delimiter * level + '}\n'
                    level -= 1

        return css.strip()

    def run(self):
        if self.args:
            for read_from in self.args:
                write_to = os.path.splitext(read_from)[0] + '.less'
                choice, content = '', ''

                if (os.path.exists(write_to)):
                    while True:
                        print '%s already exists, overwrite? (y/n):' % write_to
                        choice = raw_input()
                        if choice in ['y', 'n', 'Y', 'N']:
                            break

                if choice not in ['n', 'N']:
                    try:
                        f = open(read_from, "r")
                        try:
                            content = f.read()
                            try:
                                f = open(write_to, "w")
                                try:
                                    f.write(self.parse(content))
                                finally:
                                    f.close()
                            except IOError:
                                print 'There was an error writing to %s.' % write_to

                        finally:
                            f.close()
                    except IOError:
                        print 'There was an error reading %s.' % read_from

        else:
            sys.stdout.write(self.parse(sys.stdin.read()))

if __name__ == '__main__':
    importer = Html2Less()
    importer.run()