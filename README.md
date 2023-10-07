# NetApp-Storage-Provision

Pre-requisites<br>
--------------------------------------------------------------------------------------------------------------------------
- RHEL Server version 9.x<br>
- Python Version: 3.11 (Other versions also should be compatible)<br>
- Run the command 'python --version' in RHEL Server to verify the version of python.<br>
- Upgrade the python version if neccessary.<br>
- Install required python libraries using below given commands in the RHEL Server.<br>
***********************************************<br>
pip install pandas<br>
pip install fabric<br>
pip install colorama<br>
***********************************************<br>
- Download the Python script file 'NetApp_Provision_Script.py' and transfer it to the RHEL Server.<br>
- Create a directory '/storage_excel' in the RHEL Server.<br>
- Download the Excel file 'Storage_LUN.xlsx' and save it in a SHARED Windows Folder with appropriate permissions.<br>
- Mount the Windows SHARED folder to '/storage_excel' directory in RHEL Server and make sure 'Storage_LUN.xlsx' Excel file is visible there.<br>
- Edit Line number 12 in the script and replace the Storage Names with yours.<br>
    print(Style.BRIGHT + Fore.CYAN + "ADKDCR9STGNTAP1\nADKDCR9STGNTAP2\nADKDCR9STGNTAP3\nADKDCR9STGNTAP4\nADKDCR9STGNTAP5\n"     + Style.RESET_ALL)<br>

--------------------------------------------------------------------------------------------------------------------------
- The script supports mapping of LUNs upto two IGROUPs. It is possible to edit the script and make it eligible to map the LUNs to any number of IGROUPs
- If the LUN Type is selected as 'DATASTORE' in the Excel sheet the script will map those LUNs to the IGROUP         'BACKUP_SERV_IGROUP' (IGROUP for Backup Media Server) by default. This is for the purpose enabling SAN backups of the VMWare DATASTORE LUNs. Below given part of the code does this.<br>
elif lun_type[i] == "DATASTORE":
    con.run('lun map -vserver ' + svm[i] + ' -volume ' + lun_name[i] + '_VOL -lun ' + lun_name[i] + '_LUN -igroup BACKUP_SERV_IGROUP' )<br>

- The 'Volume Size' column in the Excel sheet will be auto populated based on the LUN Size provided using below given formula. The Excel sheet is protected in order to avoid accidental deletion of the Formula.<br>
=IF(B2<=500,B2+B2/100*20) + IF( (B2>500) * (B2<=1000),B2+B2/100*15) + IF( (B2>1000) * (B2<=3000),B2+B2/100*10) + IF( (B2>3000) * (B2<=6000),B2+B2/100*8) + IF( (B2>6000) * (B2<=9000),B2+B2/100*6) + IF( (B2>9000) * (B2<=13000),B2+B2/100*5) + IF( (B2>13000) * (B2<=16000),B2+B2/100*4)<br>

- Populate the Excel spreadsheet as shown in the video.<br>
- Execute the Python script in RHEL Server using the command 'python3.11 NetApp_Provision_Script.py'<br>
- Login to NetApp Storage Console and verify the LUNs created.<br>

Feel free to contact me on "www.linkedin.com/in/nissin-thomas" for any help.<br>
