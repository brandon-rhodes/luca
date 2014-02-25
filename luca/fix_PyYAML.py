"""PyYAML considers it a `wontfix` that it cannot actually read valid YAML.

http://pyyaml.org/ticket/169

"""
import yaml
from yaml.constructor import ConstructorError, MappingNode

class Loader(yaml.SafeLoader):
    """Allow YAML sequences to be mapping keys, per the standard."""

    def construct_mapping(self, node, deep=False):
        if not isinstance(node, MappingNode):
            raise ConstructorError(None, None,
                    "expected a mapping node, but found %s" % node.id,
                    node.start_mark)
        mapping = {}
        for key_node, value_node in node.value:
            key = self.construct_object(key_node, deep=True)
            if isinstance(key, list):
                key = tuple(key)
            value = self.construct_object(value_node, deep=deep)
            mapping[key] = value
        return mapping

if __name__ == '__main__':
    tricky = (u'{[ New York Yankees, Atlanta Braves ]:'
              u' [ 2001-07-02, 2001-08-12, 2001-08-14 ] } ')
    print(repr(yaml.load(tricky, Loader=Loader)))
