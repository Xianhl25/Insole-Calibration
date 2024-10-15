'''
关于Camargo数据集：
    * fp：地面反力数据，其中`Treadmill_R_px`表示左右方向，`Treadmill_R_pz`表示前后方向
    * gon：角度计，只在右脚上安装
    * id：逆动力学
    * ik： 逆运动学
    * imu：躯干、大腿、小腿以及脚的IMU数据
    * jp：通过关节扭矩和关节角速度估计关节功率
'''

AB09 = {
    'Name': 'AB09',
    'Sex': 'Female',
    'Height': 1.63,
    'Weight': 63.5,
}

AB10 = {
    'Name': 'AB10',
    'Sex': 'Male',
    'Height': 1.75,
    'Weight': 83.9,
}

sensor_mapping = {
    # imu on trunk 
    'I0':  'Pitch of Trunk',
    'I1':  'Roll of Trunk', # 对应矢状面上的角度
    'I2':  'Yaw of Trunk', 
    'I3':  'Gyro of x-axis',
    'I4':  'Gyro of y-axis', # 
    'I5':  'Gyro of z-axis',
    'I6':  'Acc of x-axis',
    'I7':  'Acc of y-axis', # 垂直方向上
    'I8':  'Acc of z-axis',
    # imu on right thigh
    'I9':  'Pitch of Right Thigh',
    'I10':  'Roll of Right Thigh', # 大腿角度
    'I11':  'Yaw of Right Thigh', 
    'I12':  'Gyro of x-axis',
    'I13':  'Gyro of y-axis', # 大腿弯曲的角速度
    'I14':  'Gyro of z-axis',
    'I15':  'Acc of x-axis',
    'I16':  'Acc of y-axis',  # 垂直方向
    'I17':  'Acc of z-axis',
    # imu on right shank
    'I18':  'Pitch of Right Shank',
    'I19':  'Roll of Right Shank', # 小腿角度
    'I20':  'Yaw of Right Shank', 
    'I21':  'Gyro of x-axis',
    'I22':  'Gyro of y-axis', # 小腿弯曲的角速度
    'I23':  'Gyro of z-axis',
    'I24':  'Acc of x-axis',
    'I25':  'Acc of y-axis', # 垂直方向
    'I26':  'Acc of z-axis',
    # imu on left thigh
    'I27':  'Pitch of Left Thigh',
    'I28':  'Roll of Left Thigh', # 大腿角度
    'I29':  'Yaw of Left Thigh', 
    'I30':  'Gyro of x-axis',
    'I31':  'Gyro of y-axis', # 大腿弯曲的角速度
    'I32':  'Gyro of z-axis',
    'I33':  'Acc of x-axis',
    'I34':  'Acc of y-axis', # 垂直方向
    'I35':  'Acc of z-axis',
    # imu on left shank
    'I36':  'Pitch of Left Shank',
    'I37':  'Roll of Left Shank', # 小腿角度
    'I38':  'Yaw of Left Shank', 
    'I39':  'Gyro of x-axis',
    'I40':  'Gyro of y-axis', # 小腿弯曲的角速度
    'I41':  'Gyro of z-axis',
    'I42':  'Acc of x-axis',
    'I43':  'Acc of y-axis', # 垂直方向
    'I44':  'Acc of z-axis',
    # insole under right foot
    'I45': 'First Row of Right Insole',
    'I46': 'Second Row of Right Insole',
    'I47': 'Third Row of Right Insole',
    'I48': 'Fourth Row of Right Insole',
    'I49': 'Fifth Row of Right Insole',
    'I50': 'Sixth Row of Right Insole',
    # insole under left foot
    'I51': 'First Row of Left Insole',
    'I52': 'Second Row of Left Insole',
    'I53': 'Third Row of Left Insole',
    'I54': 'Fourth Row of Left Insole',
    'I55': 'Fifth Row of Left Insole',
    'I56': 'Sixth Row of Left Insole',
}

sensor_mapping2 = { # 鞋垫数据只有第一行和最后一行的数据以及经过校准后的合力数据
    # imu on trunk 
    'I0':  'Pitch of Trunk',
    'I1':  'Roll of Trunk', # 对应矢状面上的角度
    'I2':  'Yaw of Trunk', 
    'I3':  'Gyro of x-axis',
    'I4':  'Gyro of y-axis', # 
    'I5':  'Gyro of z-axis',
    'I6':  'Acc of x-axis',
    'I7':  'Acc of y-axis', # 垂直方向上
    'I8':  'Acc of z-axis',
    # imu on right thigh
    'I9':  'Pitch of Right Thigh',
    'I10':  'Roll of Right Thigh', # 大腿角度
    'I11':  'Yaw of Right Thigh', 
    'I12':  'Gyro of x-axis',
    'I13':  'Gyro of y-axis', # 大腿弯曲的角速度
    'I14':  'Gyro of z-axis',
    'I15':  'Acc of x-axis',
    'I16':  'Acc of y-axis',  # 垂直方向
    'I17':  'Acc of z-axis',
    # imu on right shank
    'I18':  'Pitch of Right Shank',
    'I19':  'Roll of Right Shank', # 小腿角度
    'I20':  'Yaw of Right Shank', 
    'I21':  'Gyro of x-axis',
    'I22':  'Gyro of y-axis', # 小腿弯曲的角速度
    'I23':  'Gyro of z-axis',
    'I24':  'Acc of x-axis',
    'I25':  'Acc of y-axis', # 垂直方向
    'I26':  'Acc of z-axis',
    # imu on left thigh
    'I27':  'Pitch of Left Thigh',
    'I28':  'Roll of Left Thigh', # 大腿角度
    'I29':  'Yaw of Left Thigh', 
    'I30':  'Gyro of x-axis',
    'I31':  'Gyro of y-axis', # 大腿弯曲的角速度
    'I32':  'Gyro of z-axis',
    'I33':  'Acc of x-axis',
    'I34':  'Acc of y-axis', # 垂直方向
    'I35':  'Acc of z-axis',
    # imu on left shank
    'I36':  'Pitch of Left Shank',
    'I37':  'Roll of Left Shank', # 小腿角度
    'I38':  'Yaw of Left Shank', 
    'I39':  'Gyro of x-axis',
    'I40':  'Gyro of y-axis', # 小腿弯曲的角速度
    'I41':  'Gyro of z-axis',
    'I42':  'Acc of x-axis',
    'I43':  'Acc of y-axis', # 垂直方向
    'I44':  'Acc of z-axis',
    # insole under right foot
    'I45': 'First Row of Right Insole',
    'I46': 'Sixth Row of Right Insole',
    'I47': 'Sum Force of Right Insole',
    # insole under left foot
    'I48': 'First Row of Left Insole',
    'I49': 'Sixth Row of Left Insole',
    'I50': 'Sum Force of Left Insole',
}

forceplate_mapping = {
    'FX1': 'Left Foot Force on x-axis',
    'FY1': 'Left Foot Force on y-axis',
    'FZ1': 'Left Foot Force on z-axis',
    'FX2': 'Right Foot Force on x-axis',
    'FY2': 'Right Foot Force on y-axis',
    'FZ2': 'Right Foot Force on z-axis',
}

insole_mapping ={
    'I0': 'Insole force of first row',
    'I1': 'Insole force of second row',
    'I2': 'Insole force of third row',
    'I3': 'Insole force of fourth row',
    'I4': 'Insole force of fifth row',
    'I5': 'Insole force of sixth row',
    'I6': 'Sum of six row',
    'Sum': 'Sum of six row',
}

insole_mapping2 = {
    'I0': '',
}

label_mapping = {
    'idle': 0,
    'walk-rampascent': 1,
    'rampascent': 2,
    'rampascent-walk': 3,
    'walk-rampdescent': 4,
    'rampdescent': 5,
    'rampdescent-walk': 6,
}

left_insole_truncate_mapping = {
    'I0': 0,
    'I1': 0,
    'I2': 0,
    'I3': 0,
    'I4': 0,
    'I5': 0,
    'I6': 0,
    'I7': 0,
    'I8': 0,
    'I9': 0,
    'I10': 0,
    'I11': 0,
    'I12': 0,
    'I13': 0, 
    'I14': 0,
    'I15': 0,
    'I16': 0,
    'I17': 0,
}

right_insole_truncate_mapping = {
    'I0': 0,
    'I1': 0,
    'I2': 0,
    'I3': 0,
    'I4': 0,
    'I5': 0,
    'I6': 0,
    'I7': 0,
    'I8': 0,
    'I9': 0,
    'I10': 0,
    'I11': 0,
    'I12': 0,
    'I13': 0, 
    'I14': 0,
    'I15': 0,
    'I16': 0,
    'I17': 0,
}