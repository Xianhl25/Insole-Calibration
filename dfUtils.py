import os
import numpy as np
from numpy import ndarray
import pandas as pd
from pandas import DataFrame
import plotly_express as px
import plotly.graph_objects as go
from scipy.ndimage import gaussian_filter1d
from scipy.interpolate import interp1d
from scipy.signal import butter, filtfilt
from const import forceplate_mapping
from const import sensor_mapping
from const import insole_mapping

def readCsv2Df(csvPath: str, sep: str) -> DataFrame:
    if(csvPath.split('.')[-1] == 'csv'):
        df = pd.read_csv(csvPath, sep=sep)
    else:
        raise ValueError("Type of file must be csv!")
    
    return df

def readXlsx2Df(xlsxPath: str) -> DataFrame:
    if(xlsxPath.split('.')[-1] == 'xlsx'):
        df = pd.read_excel(xlsxPath)
    else:
        raise ValueError("Type of file must be xlsx!")

    return df 

def visualizeData(fig, X: ndarray, Y: ndarray, visualizationMode='lines', lineName=None, isShow=False) -> None:
    fig.add_trace(go.Scatter(
        x=X,
        y=Y,
        mode=visualizationMode,
        name=lineName,
    ))
    if isShow:
        fig.show() # 如果绘制多条曲线，isShow=True的话就会画一条曲线显示一次图像

def clipDataAndSave(df: DataFrame, startIndex: int, endIndex: int, savePath: str) -> None:
    '''
    * 为了避开开始的加速阶段和结束的减速阶段，一般跳过前6个步态周期和后6个步态周期
    '''
    if os.path.isfile(savePath): # 防止覆盖
        raise RuntimeError(f"{savePath} is not empty!")
    else:
        dfSubset = df.iloc[startIndex-1:endIndex]
        dfSubset.to_excel(savePath, index=False)
        print(f"File have saved to: {savePath}")
        print(f"Row of the clipped file: {len(dfSubset)}")

def extractGaitCycles(df: DataFrame, columnName: str) -> tuple:
    '''
    * 该函数主要是将支撑相数据按步态周期分别存在tuple中
    * clip原始数据的时候最好clip完整，可以从第一个支撑相前的摆动相开始，最后一个支撑相后的摆动相结束
    * 如果出现目标周期数与实际周期数不符的情况，可能是个别步态周期的摆动相数值会出现浮动的情况，可以通过增加鞋垫无受力下的值解决
    '''
    gaitStartIndices = np.where(np.diff((df[columnName] > 0).astype(int)) == 1)[0] + 1 # 力从0变为非零的位置对应于支撑相开始
    gaitEndIndices = np.where(np.diff((df[columnName] > 0).astype(int)) == -1)[0] + 1 # 力从非零变为0的位置对应于支撑相结束
    # print("Gait start indices: ", gaitStartIndices)
    # print("Gait end indices: ", gaitEndIndices)
    ## 如果第一个周期是未结束的，删除它
    if gaitStartIndices[0] > gaitEndIndices[0]:
        gaitEndIndices = gaitEndIndices[1:]
    ## 如果最后一个周期是未结束的，删除它
    if len(gaitStartIndices) > len(gaitEndIndices):
        gaitStartIndices = gaitStartIndices[:-1]
    gaitCycles = []
    for start, end in zip(gaitStartIndices, gaitEndIndices):
        gaitCycles.append(df.iloc[start:end]) # 将每个步态周期的数据放到元组中

    return gaitCycles

def interpolatePerCycle(gaitCycle: DataFrame, numOfPoints: int) -> DataFrame:
    '''
    * 该函数主要是将步态周期数据插值成固定长度，便于校准
    '''
    x_original = np.linspace(0, 1, len(gaitCycle)) # 原始点的相对位置
    x_interpolated = np.linspace(0, 1, numOfPoints) # 插值后的相对位置
    interpolated_values = interp1d(x_original, gaitCycle, kind='linear')(x_interpolated)

    return interpolated_values

def downsampleData(originalData: DataFrame, downsampleRate: int, savePath : str =None) -> DataFrame:
    df_downsampled = originalData.iloc[::downsampleRate, :].reset_index(drop=True)
    if savePath is not None:
        if os.path.isfile(savePath):
            raise RuntimeError(f"{savePath} is not empty!")
        else:
            if savePath.split('.')[-1] == 'xlsx':
                df_downsampled.to_excel(savePath, index=False)
                print(f"File have saved to: {savePath}")
                return df_downsampled
            elif savePath.split('.')[-1] == 'csv':
                df_downsampled.to_csv(savePath)
                print(f"File have saved to: {savePath}")
                return df_downsampled
            else:
                raise RuntimeError("Type of the save file is not supported!")

def mergeData(df_tuple: tuple, columns_to_select: dict, mergeOn: str, save_path: str) -> DataFrame:
    '''
    * format of the columns_to_select dict:
    * 'df1': ['Header', ...]
    * 'df2': ['Header', ...]
    * 'dfn': ['Header', ...]
    * where 'Header' is the mergeOn for function pd.merge
    '''
    selected_dfs = []
    for idx, df in enumerate(df_tuple):
        df_name = f'df{idx+1}'
        cols = columns_to_select[df_name]
        selected_dfs.append(df[cols])
    merged_df = selected_dfs[0]
    for df in selected_dfs[1:]:
        merged_df = pd.merge(merged_df, df, on=mergeOn, how='inner')
    merged_df.to_excel(save_path, index=False)
    print(f"Merged dataframe has been saved in {save_path}")

def lowpassFilter(original_data: DataFrame, cutoff_frequency: int, sampling_rate: int, order: int) -> DataFrame:
    b, a = butter(order, cutoff_frequency / (0.5 * sampling_rate), btype='low')
    filtered_data = filtfilt(b, a, original_data)
    return filtered_data

def gaussianFilter(original_data: DataFrame, sigma: int) -> DataFrame:
    filtered_data = gaussian_filter1d(original_data, sigma)
    return filtered_data

def truncateData(original_data: DataFrame, threshold: any) -> DataFrame:
    '''
    value smaller than threshold will be truncated to zero
    '''
    truncated_data = np.where(original_data < threshold, 0, original_data)
    return truncated_data