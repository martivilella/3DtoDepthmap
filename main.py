import open3d as o3d
import numpy as np
import os
import sys
import cv2 as cv

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
    

def main(inpath):
    # set in/out paths
    filepath,fullflname = os.path.split(inpath)
    fname,ext = os.path.splitext(fullflname)
    outdepthpath=os.path.dirname(filepath)+'depth/'+fname+'.png'
    outdeptharraypath=os.path.dirname(filepath)+'depthnpy/'+fname+'.npy'
    outsegmaskpath=os.path.dirname(filepath)+'segmask/'+fname+'.png'

    # load properties
    ## mesh
    mesh = o3d.io.read_triangle_mesh(inpath)
    mesh.compute_vertex_normals()
    
    ## camera params
    w=1000
    h=1000
    f=3000
    cam_params=o3d.camera.PinholeCameraParameters()
    cam_params.intrinsic.set_intrinsics(w, h, f, f, w/2.0-0.5, h/2.0-0.5) # TODO Adjust
    extr = np.identity(4,dtype=np.float64) # TODO Adjust
    extr[2,3] = 100
    cam_params.extrinsic=extr
    
    # create open3d visualiser
    vis = create_visualiser(mesh, cam_params)
    #vis.run()
    #vis.destroy_window()

    # capture depth img
    depth = vis.capture_depth_float_buffer(True)
    depth2darray = np.asarray(depth) # Depth in mm
    depthsize = np.shape(depth2darray)
    deptharray = np.reshape(depth2darray, (depthsize[0], depthsize[1], 1)) # reshape to 3D array
    #print(f"max={np.max(depth2darray):f}, min={np.min(depth2darray):f}")
    
    # save outputs
    ## npy depth array
    np.save(outdeptharraypath, deptharray)

    ## png depth map
    cv.imwrite(outdepthpath,np.round(deptharray*1000).astype(np.uint16))

    ## png segmask
    cv.imwrite(outsegmaskpath, deptharray.astype(bool)*255)
    
    ## intrinsic camera params
    write_intr_file("virtualcam.intr", cam_params.intrinsic)

if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Provide exactly one CLI arg as the relative path to the 3D model to load\n")
    else:
        main(sys.argv[1])