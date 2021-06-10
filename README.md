# Usage
0. (Optional) create a virtual environment to avoid dependencies conflicts with other projects
1. Install pip dependencies from ```requirements.txt```
2. Run using ```python3 main.py <3dmodel.obj>```

NB: If using a virtual environment, don't forget to activate it by sourcing from the terminal: 
```
source <venv_name>/bin/activate
```

# Supported 3D model file types
The script is using the [Open3D](https://github.com/intel-isl/Open3D) library, which supports 3D geometry file formats:
- OBJ
- PLY
- STL
- ASSIMP
- FBX
- GLTF
- OFF

Additionally, pointcloud formats are supported. These require editing the import call to convert them to a mesh:
- PCD
- PTS
- XYZ
- XYZN
- XYZRGB