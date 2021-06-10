import open3d as o3d
import numpy as np
import os
import sys
import cv2 as cv

def create_visualiser(mesh, camera_parameters):
    vis = o3d.visualization.Visualizer()
    vis.create_window()
    vis.add_geometry(mesh)
    vis.get_view_control().convert_from_pinhole_camera_parameters(camera_parameters, True) # allow arbitrary camera width/height
    return vis

def main(inpath):
    # set in/out paths
    filepath,fullflname = os.path.split(inpath)
    fname,ext = os.path.splitext(fullflname)
    outdepthpath=os.path.dirname(filepath)+'depth/'+fname+'.png'
    outdeptharraypath=os.path.dirname(filepath)+'depthnpy/'+fname+'.npy'
    outsegmaskpath=os.path.dirname(filepath)+'segmask/'+fname+'.png'

    # load mesh
    mesh = o3d.io.read_triangle_mesh(inpath)
    mesh.compute_vertex_normals()

    # load camera params
    w=1000
    h=1000
    f=3000
    cam_params=o3d.camera.PinholeCameraParameters()
    cam_params.intrinsic.set_intrinsics(w, h, f, f, w/2.0-0.5, h/2.0-0.5) # TODO Adjust
    extr = np.identity(4,dtype=np.float64) # TODO Adjust
    extr[2,3] = 100
    cam_params.extrinsic=extr
    
    vis = create_visualiser(mesh, cam_params)
    
    # visualise obj
    #vis.run()
    #vis.destroy_window()

    # capture depth img
    depth = vis.capture_depth_float_buffer(True)
    deptharray = np.asarray(depth) # Depth in mm
    print(f"max={np.max(np.asarray(depth)):f}, min={np.min(np.asarray(depth)):f}")
    
    # save outputs
    ## npy depth array
    np.save(outdeptharraypath, deptharray) 
    ## png depth map
    cv.imwrite(outdepthpath,np.round(deptharray*1000).astype(np.uint16))
    ## png segmask
    cv.imwrite(outsegmaskpath, deptharray.astype(bool)*255)

    # save intrinsic camera params in UC Berkeley GQCNN format
    fxy = cam_params.intrinsic.get_focal_length()
    cxy = cam_params.intrinsic.get_principal_point()
    intr_file = open("virtualcam.intr", "w")
    intr_file.write(f'{{"_cy": {cxy[1]:f}, "_cx": {cxy[0]:f}, "_fy": {fxy[1]:f}, "_height": {cam_params.intrinsic.height}, "_fx": {fxy[1]:f}, "_width": {cam_params.intrinsic.width}, "_skew": {cam_params.intrinsic.get_skew():f}, "_K": {0}, "_frame": "virtualcam"}}') # no distortion
    intr_file.close()
    
if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Provide exactly one CLI arg as the relative path to the 3D model to load\n")
    else:
        main(sys.argv[1])