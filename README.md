# Description
The goal of this utility is to provide a simple way to generate depth maps (Z-Buffers) from 3D models, to be used as synthetic inputs for neural networks and other relevant tasks.
It provides:
- Depth map in [m] as a 3D ```npy``` file;
- Depth map in ```png``` format with a user-defined scaling factor (default = 1000.0), so that 255RGB corresponds to 255[mm] depth; 
- Segmentation mask in ```png``` format;
- Intrinsic camera parameters in format used in the CQCNN package by [Berkeley Automation](https://github.com/berkeleyautomation)

There are numerous standards used to express depth data, so the code is designed to be modular and easy to edit for custom implementations

# Getting started
This project is developed with Python 3.8, although >=3.6 should be compatible.

To set up the project:
1. (Optional) create a virtual environment to avoid dependencies conflicts with other projects
2. Install pip dependencies from ```requirements.txt```


# Usage
Run ```main.py``` with 1 arg providing the relative path to the 3D model file:
```
python3 main.py <3dmodel.obj>
```

If using a Python virtual environment, don't forget to activate it by sourcing from the terminal: 
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