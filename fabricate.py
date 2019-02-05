import os
import re
import sys


class Fabricate:
    def __init__(self, proj_dir):
        self.proj_dir = proj_dir
        self.headers = []  # header files
        self.sources = []  # source files
        self.dependencies = {}  # source depends on what headers
        self.pairs = []  # header and sources with same root
        self.dep_regex = re.compile(r"#include\s*\"(\S*)\"")

    def __get_sources(self):
        for root, dirs, files in os.walk(self.proj_dir):
            for file in files:
                full = os.path.join(root, file)
                if file.endswith(".c"):
                    self.sources.append(full)
                    self.dependencies[full] = []
                elif file.endswith(".h"):
                    self.headers.append(full)

        print(self.sources)

    def __build_tree(self):
        for source in self.sources:
            f = open(source, "r")
            for line in f.readlines():
                m = self.dep_regex.match(line)

                if m:
                    self.dependencies[source].append(m.group(1))

            f.close()

        for key in self.dependencies.keys():
            print("{}: ".format(key), self.dependencies[key])

    def __build_pairs(self):
        for source in self.sources:
            for header in self.headers:
                if source[:source.rfind(".")] == header[:header.rfind(".")]:
                    self.pairs.append([header, source])
                    self.headers.remove(header)
                    self.sources.remove(source)


    def __compile(self):
        obj_str = ""
        for header, source in self.pairs:
            os.system("{} -c {} {}".format("gcc", header, source))

        for source in self.sources:
            os.system("{} -c {}".format("gcc", source))

        for file in os.listdir("."):
            if file.endswith(".o"):
                obj_str += file + " "

        os.system("{} -o main {}".format("gcc", obj_str))

    def build(self):
        self.__get_sources()
        self.__build_tree()
        self.__compile()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    f = Fabricate(sys.argv[1])
    f.build()
