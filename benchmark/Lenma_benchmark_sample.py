import sys
sys.path.append('../')
from logparser import LenMa, evaluator
import os
import pandas as pd

benchmark_settings = {
    'HDFS': {
        'log_file': 'HDFS/HDFS_2k.log',
        'log_format': '<Date> <Time> <Pid> <Level> <Component>: <Content>',
        'regex': [r'blk_-?\d+', r'(\d+\.){3}\d+(:\d+)?'],
        'st': 0.5,
        'depth': 4
        },

    'Hadoop': {
        'log_file': 'Hadoop/Hadoop_2k.log',
        'log_format': '<Date> <Time> <Level> \[<Process>\] <Component>: <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'st': 0.5,
        'depth': 4
        },

    'Spark': {
        'log_file': 'Spark/Spark_2k.log',
        'log_format': '<Date> <Time> <Level> <Component>: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'\b[KGTM]?B\b', r'([\w-]+\.){2,}[\w-]+'],
        'st': 0.5,
        'depth': 4
        },

    'Zookeeper': {
        'log_file': 'Zookeeper/Zookeeper_2k.log',
        'log_format': '<Date> <Time> - <Level>  \[<Node>:<Component>@<Id>\] - <Content>',
        'regex': [r'(/|)(\d+\.){3}\d+(:\d+)?'],
        'st': 0.5,
        'depth': 4
        },

    'BGL': {
        'log_file': 'BGL/BGL_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <Node> <Time> <NodeRepeat> <Type> <Component> <Level> <Content>',
        'regex': [r'core\.\d+'],
        'st': 0.5,
        'depth': 4
        },

    'HPC': {
        'log_file': 'HPC/HPC_2k.log',
        'log_format': '<LogId> <Node> <Component> <State> <Time> <Flag> <Content>',
        'regex': [r'=\d+'],
        'st': 0.5,
        'depth': 4
        },

    'Thunderbird': {
        'log_file': 'Thunderbird/Thunderbird_2k.log',
        'log_format': '<Label> <Timestamp> <Date> <User> <Month> <Day> <Time> <Location> <Component>(\[<PID>\])?: <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'st': 0.5,
        'depth': 4
        },

    'Windows': {
        'log_file': 'Windows/Windows_2k.log',
        'log_format': '<Date> <Time>, <Level>                  <Component>    <Content>',
        'regex': [r'0x.*?\s'],
        'st': 0.7,
        'depth': 5
        },

    'Linux': {
        'log_file': 'Linux/Linux_2k.log',
        'log_format': '<Month> <Date> <Time> <Level> <Component>(\[<PID>\])?: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'\d{2}:\d{2}:\d{2}'],
        'st': 0.39,
        'depth': 6
        },

    'Andriod': {
        'log_file': 'Andriod/Andriod_2k.log',
        'log_format': '<Date> <Time>  <Pid>  <Tid> <Level> <Component>: <Content>',
        'regex': [r'(/[\w-]+)+', r'([\w-]+\.){2,}[\w-]+', r'\b(\-?\+?\d+)\b|\b0[Xx][a-fA-F\d]+\b|\b[a-fA-F\d]{4,}\b'],
        'st': 0.2,
        'depth': 6
        },

    'HealthApp': {
        'log_file': 'HealthApp/HealthApp_2k.log',
        'log_format': '<Time>\|<Component>\|<Pid>\|<Content>',
        'regex': [],
        'st': 0.2,
        'depth': 4
        },

    'Apache': {
        'log_file': 'Apache/Apache_2k.log',
        'log_format': '\[<Time>\] \[<Level>\] <Content>',
        'regex': [r'(\d+\.){3}\d+'],
        'st': 0.5,
        'depth': 4
        },

    'Proxifier': {
        'log_file': 'Proxifier/Proxifier_2k.log',
        'log_format': '\[<Time>\] <Program> - <Content>',
        'regex': [r'<\d+\ssec', r'([\w-]+\.)+[\w-]+(:\d+)?', r'\d{2}:\d{2}(:\d{2})*', r'[KGTM]B'],
        'st': 0.6,
        'depth': 3
        },

    'OpenSSH': {
        'log_file': 'OpenSSH/OpenSSH_2k.log',
        'log_format': '<Date> <Day> <Time> <Component> sshd\[<Pid>\]: <Content>',
        'regex': [r'(\d+\.){3}\d+', r'([\w-]+\.){2,}[\w-]+'],
        'st': 0.6,
        'depth': 5
        },

    'OpenStack': {
        'log_file': 'OpenStack/OpenStack_2k.log',
        'log_format': '<Logrecord> <Date> <Time> <Pid> <Level> <Component> \[<ADDR>\] <Content>',
        'regex': [r'((\d+\.){3}\d+,?)+', r'/.+?\s', r'\d+'],
        'st': 0.5,
        'depth': 5
        },

    'Mac': {
        'log_file': 'Mac/Mac_2k.log',
        'log_format': '<Month>  <Date> <Time> <User> <Component>\[<PID>\]( \(<Address>\))?: <Content>',
        'regex': [r'([\w-]+\.){2,}[\w-]+'],
        'st': 0.7,
        'depth': 6
        },
}

input_dir = '../../Data/' # The input directory of log file
output_dir = 'result/' # The output directory of parsing results

HDFS_dir = 'HDFS/'
Hadoop_dir = 'Hadoop/'
Spark_dir = 'Spark/'
Zookeeper_dir = 'Zookeeper/'
BGL_dir = 'BGL/'
HPC_dir = 'HPC/'
Thunderbird_dir = 'Thunderbird/'
Windows_dir = 'Windows/'
Linux_dir = 'Linux/'
Android_dir = 'Android/'
Apache_dir = 'Apache/'
OpenSSH_dir = 'OpenSSH/'
OpenStack_dir = 'OpenStack/'
Mac_dir = 'Mac/'
HealthApp_dir = 'HealthApp/'
Proxifier_dir = 'Proxifier/'

HDFS_file = 'HDFS.log'
Hadoop_file = 'Hadoop.log'
Spark_file = 'Spark.log'
Zookeeper_file = 'Zookeeper.log'
BGL_file = 'BGL.log'
HPC_file = 'HPC.log'
Thunderbird_file = 'Thunderbird.log'
Windows_file = 'Windows.log'
Linux_file = 'Linux.log'
Android_file = 'Android.log'
Apache_file = 'Apache.log'
OpenSSH_file = 'SSH.log'
OpenStack_file = 'OpenStack.log'
Mac_file = 'Mac.log'
HealthApp_file = 'HealthApp.log'
Proxifier_file = 'Proxifier.log'

HDFS_num = 10
Hadoop_num = 10
Spark_num = 10
Zookeeper_num = 10
BGL_num = 10
HPC_num = 10
Thunderbird_num = 10
Windows_num = 10
Linux_num = 5
Android_num = 10
OpenSSH_num = 10
OpenStack_num = 6
Mac_num = 9
HealthApp_num = 10
#Proxifier_num = 10

eventcount_group = [2, 3, 4, 5, 6, 7, 8, 9, 10]

setting = benchmark_settings['Zookeeper']

bechmark_result = []
for index in range(0,Zookeeper_num,1):
    logfile = Zookeeper_file + '.part' + str(index)
    indir = input_dir + Zookeeper_dir
    log_file = os.path.basename(setting['log_file'])

    threshold = 0.5
    while threshold <= 1:
        para_info = str(threshold)
        print(para_info)
	parser = LenMa.LogParser(log_format=setting['log_format'], indir=indir, outdir=output_dir, rex=setting['regex'], threshold=threshold)
        parser.parse(logfile)
        F1_measure, accuracy = evaluator.evaluate_sample(
                       groundtruth=os.path.join('../Groundtruth', log_file + '_structured.csv'),
                       parsedresult=os.path.join(output_dir, logfile + '_structured.csv')
                       )
        bechmark_result.append([logfile, para_info, F1_measure, accuracy])
        threshold = threshold + 0.05    

df_result = pd.DataFrame(bechmark_result, columns=['Dataset', 'Para', 'F1_measure', 'Accuracy'])
print(df_result)
df_result.T.to_csv('Lenma_sample_result.csv')
