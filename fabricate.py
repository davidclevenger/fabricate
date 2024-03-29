import os
import re
import sys


class Fabricate:
    def __init__(self, proj_dir):
        self.proj_dir = proj_dir
        self.headers = []  # header files
        self.sources = []  # source files
        self.dependencies = {}  # source depends on what headers
        self.targets = []  # sources with a 'main' method defined

        self.depend_regex = re.compile(r"#include\s*\"(\S*)\"")  # match neighbor headers
        self.target_regex = re.compile(r"int\s*\n?\s*main")  # determine if file is a target
        self.fab_target_regex = re.compile(r"^(\w+)\n?") # targets in Fabfile
        self.fab_object_regex = re.compile(r"^(\w+).o\n?") # objects in Fabfile

        self.fabfile = None

    # under development
    def __read_fabfile(self):
        fab_path = os.path.join(self.proj_dir, "Fabfile")
        if os.path.exists(fab_path):
            with open(fab_path, "r") as f:
                for line in f.readlines():
                    m = self.fab_object_regex.match(line)
                    if m:
                        print("object: ", m.group(1))

                    m = self.fab_target_regex.match(line)
                    if m:
                        print("target: ", m.group(1))

                f.close()

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
                m = self.depend_regex.match(line)

                if m:
                    self.dependencies[source].append(m.group(1))

                m = self.target_regex.match(line)
                if m:
                    self.targets.append(source)
            f.close()

        print("Targets:")
        for target in self.targets:
            print(target)

        print("\nDependencies")
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
            stripped = list(set(["-I" + base for base in stripped]))
            dep_str = " ".join(stripped)

            exec_string = "{} -c {} {}".format("gcc", source, dep_str)
            print(exec_string)
            os.system(exec_string)

        # if no targets exist, stop with object creation
        if len(self.targets) == 0:
            return

        for file in os.listdir("."):
            if file.endswith(".o"):
                obj_str += file + " "

        exec_string = "{} -o main {}".format("gcc", obj_str)
        print(exec_string)
        os.system(exec_string)

    def build(self):
        """
        Perform all operations to generate objects and executable if applicable
        """
        # self.__read_fabfile()
        self.__get_sources()
        self.__build_tree()
        self.__resolve_deps()
        self.__compile()

def main():
    if len(sys.argv) != 2:
        return 1

    f = Fabricate(sys.argv[1])
    f.build()
    return 0

if __name__ == "__main__":
    sys.exit(main())
