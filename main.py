import pandas as pd
import csv
import json
import sys
import math
import numpy as np
from flask import Flask, render_template, request, redirect, Response
import random, json

original_data = pd.read_csv("Data.csv",encoding = "latin")
L=list(set(original_data['Target']))
L.sort()
L
M=list(set(original_data['Source']))
M.sort()
data_lists={}
data_lists['symptoms']=L
data_lists['diseases']=M
data_lists
# def read_data():
#     print("IN main.read_data")
#     original_data = pd.read_csv("Data.csv",encoding = "latin")
#     data=original_data.set_index("Target")
#     return original_data

def symptom_nodes(temp_data):
    print("IN main.symptom_nodes")
    df=temp_data
    df = df.sample(frac=1).reset_index(drop=True) #shuffling the data
    symptoms=pd.DataFrame(df['Target'].drop_duplicates(keep='first', inplace=False).reset_index(drop=True))
    symptoms.rename(columns={'Target':'id'},inplace=True)
    temp_frame=pd.DataFrame([*range(0,symptoms.shape[0],1)])
    symptoms['x']=temp_frame%25
    symptoms['y']=np.floor(temp_frame/25)
    symptoms['size']=1
    symptoms['color']='#008cc2'
    symptoms['label']=symptoms['id']
    symptoms['grid_x']=temp_frame%25
    symptoms['grid_y']=np.floor(temp_frame/25)
    symptoms['grid_size']=1
    symptoms['grid_color']='#008cc2'
    #shuffling nodes
    symptoms=symptoms.sample(frac=1).reset_index(drop=True)
    symptoms_dict=symptoms.to_dict(orient='records')
    graphs={}
    graphs['nodes']=symptoms_dict
    graphs['edges']=[]
    return graphs

def diseases_nodes(temp_data):
    print("IN main.diseases_nodes")
    df=temp_data
    df = df.sample(frac=1).reset_index(drop=True) #shuffling the data
    diseases=pd.DataFrame(df['Source'].drop_duplicates(keep='first', inplace=False).reset_index(drop=True))
    diseases.rename(columns={'Source':'id'},inplace=True)
    temp_frame=pd.DataFrame([*range(0, diseases.shape[0],1)])
    diseases['x']=temp_frame%15
    diseases['y']=np.floor(temp_frame/15)
    diseases['size']=1
    diseases['color']='#f75539'
    diseases['label']=diseases['id']
    diseases['grid_x']=temp_frame%15
    diseases['grid_y']=np.floor(temp_frame/15)
    diseases['grid_size']=1
    diseases['grid_color']='#f75539'
    #shuffling nodes
    diseases=diseases.sample(frac=1).reset_index(drop=True)
    diseases_dict=diseases.to_dict(orient='records')
    graphs={}
    graphs['nodes']=diseases_dict
    graphs['edges']=[]
    return graphs


def create_graph(temp_data):
    print("IN main.create_graph")
    df=temp_data
    df = df.sample(frac=1).reset_index(drop=True) #shuffling the data
    diseases=pd.DataFrame(df['Source'].drop_duplicates(keep='first', inplace=False).reset_index(drop=True)) 
    symptoms=pd.DataFrame(df['Target'].drop_duplicates(keep='first', inplace=False).reset_index(drop=True))
    symptoms.rename(columns={'Target':'id'},inplace=True)
    diseases.rename(columns={'Source':'id'},inplace=True)
    # symptoms['x']=[*range(-202*10, 203*10, 10)]
    # symptoms['y']=0
    temp_frame=pd.DataFrame([*range(0, symptoms.shape[0],1)])
    symptoms['x']=temp_frame%50
    symptoms['y']=np.floor(temp_frame/50)
    symptoms['size']=0.5
    symptoms['color']='#008cc2'
    symptoms['grid_x']=temp_frame%50
    symptoms['grid_y']=np.floor(temp_frame/50)
    symptoms['grid_size']=0.5
    symptoms['grid_color']='#008cc2'
    symptoms['label']=symptoms['id']
    # diseases['x']=[*range(-74*20, 75*20,20)]
    # diseases['y']=1000
    temp_frame=pd.DataFrame([*range(0, diseases.shape[0],1)])
    diseases['x']=temp_frame%50+1
    diseases['y']=np.floor(temp_frame/50)+20
    diseases['size']=0.5
    diseases['color']='#f75539'
    diseases['grid_x']=temp_frame%50+1
    diseases['grid_y']=np.floor(temp_frame/50)+20
    diseases['grid_size']=0.5
    diseases['grid_color']='#f75539'
    diseases['label']=diseases['id']
    # symptoms.loc[1::2,"y"] = 80
    # symptoms.loc[2::3,"y"] = 160
    # symptoms.loc[3::4,"y"] = 240
    # diseases.loc[1::2,"y"] = 900
    # diseases.loc[2::3,"y"] = 800
    nodes=symptoms.append(diseases)
    #shuffling nodes
    nodes=nodes.sample(frac=1).reset_index(drop=True)
    df=temp_data 
    edges=df.rename(columns={'Source':'target','Target':'source'})
    edges['type']='line'
    edges['color']='#736563'
    edges['size']=1
    edges['id']=[*range(0,edges.shape[0] ,1)]
    nodes_dict=nodes.to_dict(orient='records')
    edges_dict=edges.to_dict(orient='records')
    graphs={}
    graphs['nodes']=nodes_dict
    graphs['edges']=edges_dict
    return graphs





def prediction(symptoms,index):
    # index contains index of the calling function 
    func=[create_graph,symptom_nodes,diseases_nodes]
    print("IN main.prediction")
    symptoms[:] = [x for x in symptoms if x != '']
    data=original_data.set_index("Target")
    if len(symptoms)==0:
        df=original_data
        return func[index](df)
    else:
        common=data.loc[symptoms[0]]
        for symptom in symptoms:
            common=pd.merge(common, data.loc[symptom], how='inner', on=['Source'])
        common=common.iloc[:, :-1*len(symptoms)]
        common.iloc[:,-1]/=common.iloc[:,-1].sum()
        common.set_axis([*common.columns[:-1], 'Probability'], axis=1, inplace=True)
        common.sort_values(by=['Probability'], ascending=False,inplace=True)
        df=original_data
        df=df[df['Source'].isin(common['Source'])].reset_index(drop=True)
        df=df[df['Target'].isin(symptoms)].reset_index(drop=True)
        df=df.merge(common)
        return func[index](df)


