import numpy as np
import open3d as o3d


pcd = o3d.io.read_point_cloud("../data/ycb/002_master_chef_can/clouds/merged_cloud.ply")
#pcd = o3d.geometry.PointCloud()
#pcd.points = o3d.utility.Vector3dVector(points)
#pcd.colors = o3d.utility.Vector3dVector(colors)
vis = o3d.visualization.Visualizer()
vis.create_window()
vis.add_geometry(pcd)
opt = vis.get_render_option()
opt.background_color = np.asarray([0.5, 0.6, 0.9])
vis.run()
vis.destroy_window()