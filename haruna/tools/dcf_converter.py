#!/usr/bin/env python3

import argparse
import re
import yaml


class PassThroughFilter:
    def filter(self, _property, value):
        return value


class PropertyValueFilter:
    def __init__(self, rule):
        self._rule = rule

    def filter(self, property, value):
        if property in self._rule:
            return self._rule[property]
        else:
            return value


class DcfConverter:
    def __init__(self, rules):
        self._rules = rules
        self._current_target_object = ''
        self._pass_through_filter = PassThroughFilter()
        self._current_filter = self._pass_through_filter

    def convert_line(self, line):
        m = re.match(r'\[(?P<target_object>.+)\]', line)
        if m:
            self.change_target_object(m.group('target_object'))
            return line
        elif self._current_target_object == '':
            return line
        else:
            m = re.match(r'(?P<name>.+)=(?P<value>.*)', line)
            if m:
                name = m.group('name')
                value = m.group('value')
                value = self._current_filter.filter(name, value)
                return None if value is None else f'{name}={value}\n'
            else:
                return line

    def change_target_object(self, name):
        self._current_target_object = name
        rule = self._rules.get(name)
        self._current_filter = self._pass_through_filter if rule is None else PropertyValueFilter(
            rule)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', dest='input', metavar='INPUT_FILE',
                        type=argparse.FileType('r'), required=True)
    parser.add_argument('-o', dest='output', metavar='OUTPUT_FILE',
                        type=argparse.FileType('w'), required=True)
    parser.add_argument('-r', dest='rules', metavar='RULES_FILE',
                        type=argparse.FileType('r'), required=True)
    args = parser.parse_args()

    rules = None if args.rules is None else yaml.safe_load(args.rules)

    converter = DcfConverter(rules)

    for line in args.input.readlines():
        line = converter.convert_line(line.replace('\r', ''))
        if line is not None:
            args.output.write(line.replace('\n', '\r\n'))
