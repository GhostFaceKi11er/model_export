import bpy
import os
import json

bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete() # 清除blender中的所有对象

from model_export.create_convex_hull import create_convex_hull
from model_export.simplify import simplify
from model_export.process_urdf import get_info_fromURDF
from model_export.export_in_worldframe import export_in_WorldFrame
import argparse

def main():
    parser = argparse.ArgumentParser(prog='test',description=(
        '''
        setup(
            name='model_export',
            version='0.1.0',        
            description='A toolpackage for 3D processing and manipulation in Python from urdf to blender', 
            author='Haitao Xu',  
            author_email='haitaoxu_tok@outlook.com', 
            url='https://github.com/GhostFaceKi11er/model_export.git',
            install_requires=[
                'bpy: 3.6.0',
                'urchin: 0.0.29(默认的最新版)',
                'numpy: 2.1.3(默认的最新版)/1.23.5', 
                'networkx: 3.4.2(默认的最新版)/2.2',
                'PyYAML: 5.4.1'
            ],
            注意: 如果电脑一开始没有numpy和networkx, 那么直接安装urchin就会自动安装这两个库. pip install urchin
            python=3.10.12,
        )

        urdf_path='./ur3e/ur3e.urdf'   输入urdf的路径
        output_foler='./data'   输入输出数据的文件夹路径

        --yaml_path='./models/franka/franka_joints.yaml'  输入yml的路径, 存储的是joints的configuration
        --output_type 指定输出文件类型. 选项: stl、glb、obj
        --decimate=0.1   输入decimate ratio来简化模型
        --create_convex_hull  输入指令创建凸包
        --joint_localframe joint启用附坐标系, 默认joint在输出的模型文件和json文件中为worldframe
        --image 输出图片预览'''), formatter_class=argparse.RawDescriptionHelpFormatter)

    def check_decimate_ratio(value):
        try:
            fvalue = float(value)
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid value: {value}. 务必是0到1之间的小数")
        
        if 0 <= fvalue <= 1:
            return fvalue
        else:
            raise argparse.ArgumentTypeError(f"Invalid value: {value}. 务必在0到1之间")

    def parse_comma_separated_floats(value):
        try:
            return [float(x) for x in value.split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid configuration: {value}, 务必按正确格式输入！")

    def parse_comma_separated_strings(value):
        try:
            return [x for x in value.split(',')]
        except ValueError:
            raise argparse.ArgumentTypeError(f"Invalid configuration: {value}, 务必按正确格式输入！")

    parser.add_argument('urdf_path', help="输入urdf的路径 示例: './ur3e/ur3e.urdf'")
    parser.add_argument('output_folder', help="输入输出数据的文件夹路径. 该文件夹中有blend文件, 每个link的stl文件, 以及存储每个link和joint的名字, xyz,rpy,visaul的文件路径, 简化后的collision的文件路径示例: --output_foler='./data'")
    
    parser.add_argument('--yaml_path', help="输入yml的路径, 存储的是joints的configuration 示例: './models/franka/franka_joints.yaml'")
    parser.add_argument('--output_type', choices=['stl', 'glb', 'obj'], default='stl', help="指定link的输出文件类型. 选项: stl、glb、obj 默认为 stl. 示例: --output_type glb")
    parser.add_argument('--decimate_ratio', type=check_decimate_ratio, help="输入decimate ratio来简化模型, 范围为(0, 1) 默认为1, 即不简化 示例: --decimate=0.1",default=1)
    parser.add_argument('--create_convex_hull', action='store_true', help="启用凸包创建功能（默认禁用）")
    parser.add_argument('--joint_localframe', action='store_true', help="joint启用附坐标系, 默认joint在输出的模型文件和json文件中为worldframe")
    parser.add_argument('--image', action='store_true', help="输出图片预览（默认不输出）")

    args = parser.parse_args()

    output_path = args.output_folder + "/output_data.json" # 输出数据的完整路径
    urdf_input_path = args.urdf_path # 输入的urdf文件的路径
    directory_path = args.output_folder #如果文件夹不存在就新建一个
    os.makedirs(directory_path, exist_ok=True)
    output_folder = args.output_folder #设置部分变量名
    yaml_path = args.yaml_path
    decimate_ratio = args.decimate_ratio 
    joint_xyzrpy_in_LocalFrame = args.joint_localframe
    output_type = args.output_type
    image = args.image

    data = get_info_fromURDF(urdf_input_path, output_path, yaml_path, joint_xyzrpy_in_LocalFrame) # 从urdf中获取数据并处理，将需要的数据导出到output_path中
    print("URDF information extracted successfully.\n")

    if args.create_convex_hull:
        create_convex_hull(data) # 对每个模型建立凸包
        print("Convex hull created successfully.\n")

    if decimate_ratio != 1:
        simplify(decimate_ratio, data) # 对每个3d模型进行简化
        print("Mesh simplified successfully.\n")


    export_in_WorldFrame(joint_xyzrpy_in_LocalFrame, output_type, output_folder, output_path, data, image) # 将处理后的3d模型和blend文件导出，并在数据json文件中更新路径
    print("Successfully export in World Frame\n")

if __name__ == "__main__":
    main()

