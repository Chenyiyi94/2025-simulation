import os, sys
import math
import numpy as np
from bmtk.simulator import pointnet   #pointnet模块
from bmtk.simulator.pointnet.pyfunction_cache import synaptic_weight  #突触权重装饰器/工具
from bmtk.simulator.pointnet.io_tools import io

import nest    #神经系统的模拟器


try:
    nest.Install('glifmodule')
except Exception as e:
    pass


@synaptic_weight    #使用synaptic weight装饰器来标记这个函数为突触权重计算函数
def DirectionRule_others(edges, src_nodes, trg_nodes):
    src_tuning = src_nodes['tuning_angle'].values   #获取源节点的tuning angle
    tar_tuning = trg_nodes['tuning_angle'].values   #目标节点的tuning angle
    sigma = edges['weight_sigma'].values    #从edges中获取weight sigma的值,权重标准差
    nsyn = edges['nsyns'].values            #从edges中获取nsyns的值，突触数量
    syn_weight = edges['syn_weight'].values #从edges中获取syn weight,初始权重值？

    delta_tuning_180 = np.abs(np.abs(np.mod(np.abs(tar_tuning - src_tuning), 360.0) - 180.0) - 180.0)    # 使用abs和mod函数来处理角度的周期性，确保差异在0-180度范围内。
    w_multiplier_180 = np.exp(-(delta_tuning_180 / sigma) ** 2)  #权重乘数随着调谐角度差异的增大而减小，sigma控制减小的速度
    
    return syn_weight * w_multiplier_180 * nsyn  #最终的突触权重=基础/初始权重*权重乘数*突触数量


@synaptic_weight
def DirectionRule_EE(edges, src_nodes, trg_nodes):
    src_tuning = src_nodes['tuning_angle'].values  #源节点和目标节点的tuning angle
    tar_tuning = trg_nodes['tuning_angle'].values
    x_tar = trg_nodes['x'].values     #源节点和目标节点的x,z坐标
    x_src = src_nodes['x'].values
    z_tar = trg_nodes['z'].values
    z_src = src_nodes['z'].values
    sigma = edges['weight_sigma'].values   #权重标准差
    nsyn = edges['nsyns'].values           #突触数量
    syn_weight = edges['syn_weight'].values   #初始权重
    
    delta_tuning_180 = np.abs(np.abs(np.mod(np.abs(tar_tuning - src_tuning), 360.0) - 180.0) - 180.0)
    w_multiplier_180 = np.exp(-(delta_tuning_180 / sigma) ** 2)

    delta_x = (x_tar - x_src) * 0.07    #源节点和目标节点在x,z方向上的位置差异
    delta_z = (z_tar - z_src) * 0.04

    theta_pref = tar_tuning * (np.pi / 180.)
    xz = delta_x * np.cos(theta_pref) + delta_z * np.sin(theta_pref)
    sigma_phase = 1.0
    phase_scale_ratio = np.exp(- (xz ** 2 / (2 * sigma_phase ** 2)))

    # To account for the 0.07 vs 0.04 dimensions. This ensures the horizontal neurons are scaled by 5.5/4 (from the
    # midpoint of 4 & 7). Also, ensures the vertical is scaled by 5.5/7. This was a basic linear estimate to get the
    # numbers (y = ax + b).
    theta_tar_scale = abs(abs(abs(180.0 - np.mod(np.abs(tar_tuning), 360.0)) - 90.0) - 90.0)
    phase_scale_ratio = phase_scale_ratio * (5.5 / 4.0 - 11.0 / 1680.0 * theta_tar_scale)

    return syn_weight * w_multiplier_180 * phase_scale_ratio * nsyn


def main(config_file):
    configure = pointnet.Config.from_json(config_file)  # 配置文件config_file
    configure.build_env()

    graph = pointnet.PointNetwork.from_config(configure)    
    sim = pointnet.PointSimulator.from_config(configure, graph)
    sim.run()


if __name__ == '__main__':
    if __file__ != sys.argv[-1]:
        main(sys.argv[-1])
    else:
        main('config.json')
