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
        """
        Locate all source files and header files within the project directory
        """
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
        """
        Build dependency trees
        """
        for source in self.sources:
            f = open(source, "r")
            for line in f.readlines():
                m = self.dep_regex.match(line)

                if m:
                    self.dependencies[source].append(m.group(1))
            f.close()

        for key in self.dependencies.keys():
            print("{}: ".format(key), self.dependencies[key])

    def __resolve(self, dep):
        """
        determine the full file path to a dependency
        """
        for header in self.headers:
            if dep in header:
                return header

        raise Warning('WARN: Unable to resolve header.')

    def __resolve_deps(self):
        """
        replace file names with full relative paths in self.dependencies
        """
        for key in self.dependencies.keys():
            resolved = []
            for dep in self.dependencies[key]:
                resolved.append(self.__resolve(dep))

            self.dependencies[key] = resolved

    @staticmethod
    def __strip(path):
        """
        Remove the last element in the path to a file or file.
        ex. (./path/to/dependency -> ./path/to)
        ex. (./a/b/c/d/e/f -> ./a/b/c/d/e)
        """
        return path[:path.rfind('/')]

    def __compile(self):
        """
        Compile the sources into objects. Then, link objects into executable.
        """
        obj_str = ""

        for source in self.sources:
            stripped = [self.__strip(path) for path in self.dependencies[source]]
            stripped = ["-I" + base for base in stripped]
            dep_str = " ".join(stripped)
            os.system("{} -c {} {}".format("gcc", source, dep_str))

        for file in os.listdir("."):
            if file.endswith(".o"):
                obj_str += file + " "

        os.system("{} -o main {}".format("gcc", obj_str))

    def build(self):
        """
        Perform all operations to generate executable
        """
        self.__get_sources()
        self.__build_tree()
        self.__resolve_deps()
        self.__compile()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(1)

    f = Fabricate(sys.argv[1])
    f.build()
