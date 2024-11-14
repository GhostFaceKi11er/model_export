# MeshMan
基于blender(3.6.5)的机器人外发模型操作工具

# 终端指令
python3 /home/haitaoxu/code/getfromURDF.py

blender --background --python /home/haitaoxu/code/toblender.py

# 代码框架


# 功能
从urdf中读取模型信息
- 简化
- 在特定姿态下更改参考坐标系为基座坐标系
- 建convex_hull

# 示例
```
./examples/simplifyMesh.py --urdf_path="models/thor3/thor3.urdf" --decimate="0.1" --output_foler="./output/" --ref_frame="base" --ref_configuration="0,0,0,1.57,0,0"
```
