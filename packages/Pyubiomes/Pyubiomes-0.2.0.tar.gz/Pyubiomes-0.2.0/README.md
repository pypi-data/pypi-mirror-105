# Pyubiomes, a Simple (wip) Python Wrapper For [Cubiomes by Cubitect](https://github.com/Cubitect/cubiomes) and other Seedfinding Utilities
## Introduction
Pyubiomes is a (relatively) easy to use, easy to understand wrapper for the Cubiomes library and minecraft_nether_generation_rs rust library, and soon to be a few more. This project is still a wip, so please mention bugs/improvements. 

If you would like to help work on this project, contact me on Discord: RamRam#0001 or join the Discord server. I still am relatively new to making Python modules, and especially seedfinding, so having an extra brain dedicated to this would be helpful so that I don't waste poor Neil's time asking stupid questions about Minecraft worldgen. This is my first Python module that uses a C extension and also my first project that uses C. Literally before starting this project, I only started learning C 2 days before.

## Installation

**NOTE: RIGHT NOW THE AUTO BUILD/INSTALL IS ONLY FOR LINUX. I AM TRYING TO FIX THAT RIGHT NOW, BUT I CAN'T GET SHIT TO COMPILE ON WINDOWS** 

If you would like to help supply build for Windows, contact me on Discord (listed above).

You can install Pyubiomes with pip using the following
```pip install Pyubiomes```

### Manual Build/Installation:
___
#### Requirements:

 - Cubiomes
 
 - [minecraft_nether_generation_rs] (github.com/SeedFinding/minecraft_nether_generation_rs) Rust libary with Python bindings (Not that hard to get)


#### Linux: 

- Clone this reposititory and [Cubiomes](https://github.com/Cubitect/cubiomes)

- install minecraft_nether_generation_rs using [these instructions](https://github.com/SeedFinding/minecraft_nether_generation_rs)

- Move the contents of the Cubiomes master branch into the `Pyubiomes-master` and rename the cubiomes master folder to "cubiomes"

- Change the current working directory to the pyubiomes master folder and run `python setup.py install`

___
### Windows:

The same as Linux, except you might get errors that I don't know how to fix.

___
### Installation Errors:

 If you get errors due to the absence of `Python.h`, here's how you might be able to fix them:


 **Linux:** 

Try to locate `Python.h` with `locate Python.h` If you can find the file located, most likely [this stackoverflow answer](stackoverflow.com/a/19344978/4954434) will work. It is likely a path issue



However, if you can't locate the file, use your package manager to install the header files and static libraries for python dev (courtesy of [this stackoverflow question](https://stackoverflowcom/questions/21530577/fatal-error-python-h-no-such-file-or-directory))

With `apt` (**Ubuntu, Debian...**)
:
`sudo apt-get install python3-dev`

For `yum` (**CentOS, RHEL...**)
:
`sudo yum install python3-devel`

For `dnf` (**Fedora...**)
:
`sudo dnf install python3-devel`

For `zypper` (**openSUSE...**)
:
`sudo zypper in python3-devel`

For `apk` (**Alpine...**)
:
`sudo apk add python3-dev `

For `apt-cyg` (**Cygwin...**)
:
`apt-cyg install python3-devel`

**Windows:**

Honestly if I knew the answer for Windows, I would've had an auto install/build for it by now. I belive `Python.h` comes with the standard Python installation, so the problem is with path variables or your compiler not checking the proper include paths. I've tried everything I could on Windows, but I couldn't get anything to work. Kind of ironic considering I use it more than Linux and know like 10 times more on Windows.

## Example Code
This example is here to give ideas on how to use these functions together to make a seedfinder, as for beginners, it may not be obvious to them at first. This is just an example. In reality, you would want to search the lower 48 bits first then find an upper 16 to meet the requirements
```python
###############
#simple example program with mutithreading
#that can find biomes and structures
###############

import Pyubiomes
from Pyubiomes import Versions, Biomes, Structures, structure_in_area, biomes_in_area, is_valid_structure_pos, get_spawn

import concurrent.futures

wanted=[Biomes.dark_forest, Biomes.savanna] #There's a bug where if you only pass a list with 1 element, the program crashes.
structure=Structures.Mansion

seeds=[]

def finder(start, increment):
	seed=start
	while True:

			print(seed)

			p=structure_in_area(structure, seed,-128, -128, 128, 128, Versions.MC_1_16) #check region for structure
			q=biomes_in_area(wanted, seed, -64, -64, 64, 64, Versions.MC_1_16) #check region for list of biomes

			if p and q: #compare the 2
				r=is_valid_structure_pos (structure, seed, p[0], p[1], Versions.MC_1_16) #if there is a structure
				if r:
					spawn=get_spawn(seed, Versions.MC_1_16)
					print(f"found seed that met requirements: {seed} with structure at {p}, and a world spawn of {spawn}")
					global seeds
					seeds.append(seed)
				if len(seeds)>=1: #make sure all threads break out of the loop
					break
			seed+=increment
				

def start(n): #ThreadPool
		with concurrent.futures.ThreadPoolExecutor(max_workers=n) as executor:
			jobs = {executor.submit(finder, *(i,n)) for i in range(n)}
		for fut in concurrent.futures.as_completed(jobs):
			print(fut.result())

start(4) #initialize

```
## Documentation:
**Note:** Code written before 0.2.0 will no longer work due to changes in naming for functions to become more pythonic
### Biome-Searching Functions:

```python
biome_at_pos(biome: int, seed: long, xpos: int, zpos: int, version: int)
```
Returns `True` if there is a `[biome]` at `(xpos, zpos)` on the seed `[seed]` in minecraft version `[version]`. Otherwise returns `False`. 


```python
biomes_in_area(biomes: list, seed: long, x1: int, z1: int, x2: int, z2: int, version: int) 
```

Returns `True` if all of the given biomes, `[biomes]` are in the rectangular area between corners `(x1,z1)` and `(x2,z2)`. Otherwise returns `False`
**Note:** The x and z values of the first point must be strictly less than the corresponding values of the second point.

### Structure Finding:
```python 
structure_in_area(structType: int, lower48: long, x1: int, z1: int, x2: int, z2: int, version: int)
```
Returns Structure Position as a tuple if the (lower 48 bits of) the seed, `[lower48]` has an attempted spawn of a structure of `[structureType]` in the rectangular region between points `(x1,z1)`, `(x2,z2)`. Otherwise returns `None`". **Note:** The x and z values of the first point must be strictly less than the corresponding values of the second point.


```python 
is_valid_structure_pos(structType: int, seed: long, structx: int, structz: int, version: int)
```
Returns `True` if the given structure type, `[structType]` has a valid spawning location at the location `(structx, structz)`. Otherwise returns `False`.

### Get World Spawnpoint

```python
get_spawn(seed: long, version: int)
```
Returns a tuple containing the x and z coordinates of the estimated worldspawn for `[seed]` in minecraft version `[version]`


### Constants
You've probably noticed that all of these functions ask for the biome, structure, etc. as an integer.

You do not need to memorize IDs to pass in as parameters, as there are keywords in a few classes.

To pass in a value for a biome into a function, you can pass in `Biomes.namespaced_id`, replacing "namespaced_id" with the namespaced id for the biome.  **Note:** for editions that use legacy names, you have to use the newer name of the biome


The same thing applies for structures, except the class you want to access is the `Structures` class, so it would be `Structures.namespaced_id`.

For the version, you can pass in `Versions.MC_1_xx`, or you can just pass in the final 2 digits of the version number. It can be more clear to people not used to the module if you use `Versions.MC_1_xx`, however.

### Nether
Thanks to [Neil](https://github.com/hube12/) for making this nether stuff possible. Neil released a new commit of minecraft_nether_generation_rs that allows it to be compatible with the old version of Rust (1.44.0) that Replit uses. Without them, this project would take many many times longer because I wouldn't be able to work on it at school. He's a really cool dude that is the leader of projects such as [minemap](https://github.com/hube12/Minemap/tree/1.0.10). The nether stuff is still wip, but so far I've gotten the ability to find biomes.
