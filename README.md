# BLFS Packages Dependency Tree Builder and Visualizer  
This is a Python code to plot a the package tree for the Beyond Linux From Scratch books.
It collects data from Linux From Scratch website and generates a visual dependency tree.

### Required Modules:
1. `bs4`: `BeautifulSoup` from the `bs4` module is used to collect data from the BLFS website.
2. `networkx`: `networkx` is used to plot the visuals. Refer [Networkx website](https://networkx.readthedocs.org/en/stable/index.html) for upstream requirements.
3. `pydotplus`: The `pydotplus` module is required for plotting and saving the visuals. Refer [pydotplus docs](http://pydotplus.readthedocs.org/) for upstream requirements.
4. `os, sys, getopt, urllib2, time`: All these should be available with most Python installations.

```
Usage: python blfs-toolchain.py [OPTIONS] [URL|DOTFILE]
URL     : BLFS book URL for which dependency tree is needed.
          Example URL: 'http://linuxfromscratch.org/blfs/view/stable/'
DOTFILE : Pregenerated dot file with the dependency tree
Possible OPTIONS are:
-h, --help            : Print this help document
-o, --outfile=<file>  : File to save dot output
-i, --imgfile=<file>  : File to save dependency tree image (use proper extension)
                        Image format can be any supported pydotplus format
                        Requires good grpahics capability on system
-d, --dependents=<pck>: Get packages which are dependent on pck
-p, --print           : Print all package names.
                        Use this to get names for <pck> for -d
```

 *If long options don't work, use short options.*
