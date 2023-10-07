import pandas as pd
import fabric
from getpass import getpass
from colorama import Fore, Back, Style, init

print(Style.BRIGHT + Fore.YELLOW + "\n*****************************************\n" + Style.RESET_ALL)
print(Style.BRIGHT + "NetApp Storage LUN Provisioning\n")
print(Style.BRIGHT + Fore.YELLOW + "*****************************************\n")
print(Style.BRIGHT + Fore.CYAN + "ADKDCR9STGNTAP1\nADKDCR9STGNTAP2\nADKDCR9STGNTAP3\nADKDCR9STGNTAP4\nADKDCR9STGNTAP5\n" + Style.RESET_ALL)
storage_name = input(Style.BRIGHT + "Storage Name: " + Style.RESET_ALL)
passwd = getpass(Style.BRIGHT + "Password: " + Style.RESET_ALL)
con = fabric.Connection(storage_name, port=22, user="admin", connect_kwargs={'password': passwd})

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
svm = df_filtered['SVM'].tolist()
vol_size = df_filtered['Volume Size'].tolist()
total_luns = (len(lun_name))

print(Fore.GREEN)
i = 0
while i < total_luns:
    con.run('vol create -volume ' + lun_name[i] + '_VOL -vserver ' + svm[i] + ' -aggregate ' + aggr_name[i] + ' -size ' + str(round(vol_size[i])) + 'g -state online -policy default -unix-permissions ---rwxr-xr-x -type RW -snapshot-policy none -foreground true -security-style unix -percent-snapshot-space 0 -space-guarantee none -autosize-mode grow_shrink -autosize-grow-threshold-percent 95 -autosize-shrink-threshold-percent 50')
    con.run('lun create -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -vserver ' + svm[i] + ' -size ' + str(round(lun_size[i])) + 'g -ostype ' + os_type[i] + ' -space-reserve disabled -space-allocation enabled')
    
    if lun_type[i] == "RDM":
        if igroup_name1[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name1[i] )
        if igroup_name2[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name2[i] )
    
    elif lun_type[i] == "DATASTORE":
        con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup BACKUP_SERV_IGROUP' )
        if igroup_name1[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name1[i] )
        if igroup_name2[i] == "No_Selection":
            pass
        else:
            con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup ' + igroup_name2[i] )
    i += 1
print(Style.RESET_ALL)