import open3d as o3d
import numpy as np
import os
import sys
import png

def create_camera(w, h, fx, fy, cx, cy, extr):
    '''
    Create [open3d.camera.PinholeCameraParameters](http://www.open3d.org/docs/release/python_api/open3d.camera.PinholeCameraParameters.html#open3d.camera.PinholeCameraParameters) object from pinhole camera parameters and extrinsic 4x4 numpy array
    '''
    cam_params=o3d.camera.PinholeCameraParameters()
    cam_params.intrinsic.set_intrinsics(w, h, fx, fy, cx, cy)
    cam_params.extrinsic=extr
    return cam_params

def create_visualiser(mesh, camera_parameters):
    '''
    Create [open3d.visualization.Visualizer](http://www.open3d.org/docs/release/python_api/open3d.visualization.Visualizer.html#open3d.visualization.Visualizer) object from geometry and intr+extr camera params
    '''
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.get_view_control().convert_from_pinhole_camera_parameters(camera_parameters, True) # allow arbitrary camera width/height
    return vis

def write_intr_file(filename, intr_params):
    '''
    Generate an intrinsic camera parameters file with the format used by the GQCNN project by UC Berkeley
    '''
    fname, ext = os.path.splitext(filename)
    fxy = intr_params.get_focal_length()
    cxy = intr_params.get_principal_point()
    intr_file = open(filename, "w")
    intr_file.write(f'{{"_cy": {cxy[1]:f}, "_cx": {cxy[0]:f}, "_fy": {fxy[1]:f}, "_height": {intr_params.height}, "_fx": {fxy[1]:f}, "_width": {intr_params.width}, "_skew": {intr_params.get_skew():f}, "_K": {0}, "_frame": "{fname}"}}') # no distortion
    intr_file.close()
    
def main(inpath, s=1000.0):
    # set in/out paths
    filepath,fullflname = os.path.split(inpath)
    fname,ext = os.path.splitext(fullflname)
    outdepthpath=os.path.dirname(filepath)+'depth/'+fname+'.png'
    outdeptharraypath=os.path.dirname(filepath)+'depthnpy/'+fname+'.npy'
    outsegmaskpath=os.path.dirname(filepath)+'segmask/'+fname+'.png'

    # create subfolders for output data
    subfolders = ['depth', 'depthnpy', 'segmask']
    for subfolder in subfolders:
        try:
            os.mkdir(subfolder)
        except:
            pass # skip if subfolder already exists

    # load properties
    ## mesh
    mesh = o3d.io.read_triangle_mesh(inpath)
    mesh.compute_vertex_normals()
    
    ## camera params
    w=1000
    h=1000
    f=3000
    extr = np.identity(4,dtype=np.float64)
    extr[2,3] = 100
    cam_params = create_camera(w, h, f, f, w/2.0-0.5, h/2.0-0.5, extr)
    
    # create open3d visualiser
    vis = create_visualiser(mesh, cam_params)
    #vis.run()
    #vis.destroy_window()

    # capture depth img
    depth = vis.capture_depth_float_buffer(True) # Depth in mm
    depth2darray = np.asarray(depth)/1000.0 # Depth in m
    depthsize = np.shape(depth2darray)
    depth3darray = np.reshape(depth2darray, (depthsize[0], depthsize[1], 1)) # reshape to 3D array
    print(f"Depth map stats: \n max: {np.max(depth2darray):f}\tm\n min: {np.min(depth2darray[depth2darray.astype(bool)]):.5f}\tm") # apply mask to min calculation, background has value of 0
    
    # save outputs
    ## npy depth array
    np.save(outdeptharraypath, depth3darray)

    ## png depth map
    png.from_array((depth2darray*s).astype(np.uint8), mode="L").save(outdepthpath)

    ## png segmask
    png.from_array((depth2darray.astype(bool)*255).astype(np.uint8), mode="L").save(outsegmaskpath)
    
    ## intrinsic camera params
    write_intr_file("virtualcam.intr", cam_params.intrinsic)

if __name__ == "__main__":
    if (sys.argv[1] == '--help' or sys.argv[1] == '-h'):
        print("Usage:\n main.py <3dmodel_path> [<depthmap_scale>]")
    elif (len(sys.argv) < 2):
        print("Provide at least one CLI arg as the relative path to the 3D model to load\n")
    elif (len(sys.argv) == 2):
        main(sys.argv[1])
    #elif (len(sys.argv) == 3):
    else:
        main(sys.argv[1], sys.argv[2])