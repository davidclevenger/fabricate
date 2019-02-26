# fabricate
Automatically determine and build C projects without a makefile

## Usage
```sh
$ python fabricate.py ./path/to/project/
```
Fabricate assumes *all* of the source code to build is located within **./path/to/project/** and its subdirectories.


## Fabfile - Under Development
If you want, you can place a *Fabfile* in the root of your project directory.

Fabfiles only contain two types of tokens, objects and targets, each on a line by themselves.

### Examples
*target only*
```
main
```

*objects only*
```
funcs.o
utils.o
```
*objects and targets*
```
driver
main
funcs.o
```

## Installation
* clone repo and copy fabricate.py to your
* I will eventually put the project on PyPi

## Motivation
When building C projects, I often found myself spending time trying to build with autotools or Cmake.
These always create headaches. Cmake is not trivial to mainitan.

Another reason is to get a project building quickly without having to create a makefile.

### Notes
* Currently only supporting C projects.
* Fabfile functionality is incomplete
