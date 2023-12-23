import re

file_name = './[your_file_name]'

srt_file = open(file_name+'.srt', mode='r', encoding='utf-8')
srt_cut_file = open(file_name+'_cut.srt', mode='w', encoding='utf-8')


cut_point = 0
for line in srt_file.readlines():
    if '-->' in line:
        line = line.strip()
        [start,end] = line.split(' --> ')
        start = re.split(':|,',start)
        end = re.split(':|,',end)
        start_point = int(start[3])+1000*int(start[2])+60*1000*int(start[1])+60*60*1000*int(start[0])
        end_point = int(end[3])+1000*int(end[2])+60*1000*int(end[1])+60*60*1000*int(end[0])
        time_difference = start_point - cut_point
        start_point = cut_point
        end_point = end_point - time_difference
        cut_point = end_point
        start = str(start_point//(60*60*1000))+':'+str(start_point%(60*60*1000)//(60*1000))+':'+str(start_point%(60*1000)//1000)+','+str(start_point%1000)
        end = str(end_point//(60*60*1000))+':'+str(end_point%(60*60*1000)//(60*1000))+':'+str(end_point%(60*1000)//1000)+','+str(end_point%1000)
        srt_cut_file.write(start + ' --> ' + end + '\n')
    else:
        srt_cut_file.write(line)

srt_file.close()
srt_cut_file.close()