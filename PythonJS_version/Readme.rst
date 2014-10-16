Conversion to Javascript
=========================

This dir contains a version of the unit convertor code that was used to convert to Javascript.

It's got a few variations to make it work with PythonJS:

 * put the UnitData in the same module, rather than importing it.
 * removed the custom exceptions -- PytonJS can't subclass from Exception. Arguably, VAlueError was a better option anyway

AT some point, it would be good to merge this into the main version, so we only have to maintain one, but that will have to wait...

PythonJS:
---------

Final working version converted with PythonJS:

https://github.com/PythonJS/PythonJS

However, PythonJS has morphed into Python* -- i.e. the same code base to convert to other languages. The developer is currently focused on Go -- so the fork with the most bug fixes is actually Gython:

https://github.com/gython/Gython

So I converted this by cloning that repo and running:

$ Gython/pythonjs/translator.py unit_conversion.py > unit_conversion.js

Also, if you want the most readable JS for debugging, you can do:

$ Gython/pythonjs/translator.py --no-wrapper --no-runtime --fast-javascript --fast-loops --pure-javascript unit_conversion.py > unit_conversion.js

though that barfs for me -- removing --pure-javascript does work, though:

$ Gython/pythonjs/translator.py --no-wrapper --no-runtime --fast-javascript --fast-loops  unit_conversion.py > unit_conversion.js

you also (may) need the pythonjs-minimal.js file:

https://github.com/gython/Gython/blob/master/pythonjs/pythonjs-minimal.js

Runing one of these commands produces:

unit_conversion.js

You can test it in node by running:

node test_unit_conversion.js 

You can see that is a pretty simple script that loads up the module with requirejs, and then accesses a couple attributes, and calls a couple funcitons, and then crashes trying to call what we really want:

uc.convert('length', 'meter', 'feet', 1.0)

Nathan found that he had to edit the generated convert() function a bit, so this probably doesn't work out of the box.


