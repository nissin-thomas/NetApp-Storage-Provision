import pandas as pd
import fabric
from getpass import getpass

passwd = getpass()
con = fabric.Connection("STORAGE IP ADDRESS", port=22, user="admin", connect_kwargs={'password': passwd})
excel_file_path = '/storage_excel/Storage_LUN.xlsx'
df1 = pd.read_excel(excel_file_path)
df_filtered = df1[df1['Volume Size'] != 0]
lun_name = df_filtered['LUN Name'].tolist()
lun_size = df_filtered['LUN Size (GB)'].tolist()
aggr_name = df_filtered['Aggregate Name'].tolist()
os_type = df_filtered['OS Type'].tolist()
igroup_name1 = df_filtered['IGROUP1'].tolist()
igroup_name2 = df_filtered['IGROUP2'].tolist()
lun_type = df_filtered['LUN Type'].tolist()
vol_size = df_filtered['Volume Size'].tolist()
total_luns = (len(lun_name))

i = 0
while i < total_luns:
    con.run('vol create -volume ' + lun_name[i] + '_VOL -vserver SVM_SAN_01_EHS -aggregate ' + aggr_name[i] + 
' -size ' + str(round(vol_size[i])) + 'g -state online -policy default -unix-permissions ---rwxr-xr-x 
-type RW -snapshot-policy none -foreground true -security-style unix -percent-snapshot-space 0 
-space-guarantee none -autosize-mode grow_shrink -autosize-grow-threshold-percent 95 
-autosize-shrink-threshold-percent 50')
    con.run('lun create -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -vserver SVM_SAN_01_EHS -size ' + str(round(lun_size[i])) + 'g -ostype ' + os_type[i] + ' -space-reserve disabled -space-allocation enabled')
    
    if lun_type[i] == "RDM":
        if igroup_name1[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver SVM_SAN_01_EHS -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name1[i] )
        if igroup_name2[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver SVM_SAN_01_EHS -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name2[i] )
    
    elif lun_type[i] == "DATASTORE":
        con.run('lun map -vserver SVM_SAN_01_EHS -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup BACKUP_SERV_IGROUP' )
        if igroup_name1[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver SVM_SAN_01_EHS -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name1[i] )
        if igroup_name2[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver SVM_SAN_01_EHS -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name2[i] )
    i += 1
