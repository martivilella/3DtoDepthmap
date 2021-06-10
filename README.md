# Usage
```
source 3DtoDepthmap-env/bin/activate
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