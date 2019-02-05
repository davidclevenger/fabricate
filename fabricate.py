import os
import re


class Fabricate:

    def __init__(self):
        self.sources = []
        self.dependencies = {}
        self.dep_regex = re.compile(r"#include\s*\"(\S*)\"")



    def getSources(self, dirpath):
        for root, dirs, files in os.walk(dirpath):
            for file in files:
                if file.endswith(".c") or file.endswith(".h"):
                    self.sources.append(os.path.join(root,file))

        print(self.sources)

    def buildTree(self):
        for source in self.sources:
            f = open(source, "r")
            for line in f.readlines():
                m = self.dep_regex.match(line)

                if m:
                    self.dependencies[source] = m.group(1)





f = Fabricate()
f.getSources("./tests/single")
f.buildTree()