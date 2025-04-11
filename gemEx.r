library(openxlsx)
folder_path = "/mnt/hdd1/hdd/OneDrive平田研共有フォルダ/Members/滝嶋遼/a/"
file_list = list.files(path = folder_path, pattern = "\\.xlsx$", full.names = TRUE)

for(data_name in file_list){
#読み込むファイル名の設定
#data_name = "/mnt/hdd1/hdd/OneDrive平田研共有フォルダ/Members/滝嶋遼/EthoVision Rawdata Excel/20200615_kcc2_3.xlsx"
#delete_name = "2023_08_01/"

{
#time = data[35:14420,1] #14420
#time = as.numeric(time)
#time=data.frame(time)
}

#移動距離、速度のデータを抽出
D = NULL
V = NULL
sheet_num = getSheetNames(data_name)
for(i in seq_along(sheet_num)){
  data = read.xlsx(data_name, sheet=i)
  TEMP.D=data[35:14420,8]
  TEMP.V=data[35:14420,9]
  TEMP.D=as.numeric(TEMP.D)
  TEMP.V=as.numeric(TEMP.V)
  TEMP.D[is.na(TEMP.D)] = 0
  TEMP.V[is.na(TEMP.V)] = 0
  for (j in 2:14386) {
    TEMP.D[j] = TEMP.D[j-1] + TEMP.D[j]
  }
  D=cbind(D,TEMP.D)
  V=cbind(V,TEMP.V)
  colnames(D)[i]=sprintf("sample-%s",i) #%s iによってsample名が変わる
  colnames(V)[i]=sprintf("sample-%s",i)
}

#データ名から無駄な部分を削除、以降使用する
data_name = gsub("/mnt/hdd1/hdd/OneDrive平田研共有フォルダ/Members/滝嶋遼/EthoVision Rawdata Excel/","",data_name)
#data_name = gsub(delete_name,"",data_name)
data_name = gsub(".xlsx","",data_name)

#移動距離、速度の保存
data_rename = paste0(data_name,"_Total_Distance")
save(D,file=data_rename)
data_rename = paste0(data_name,"_Velocity")
save(V,file=data_rename)
#save(time,file="time_behavior")

#平均速度を算出
window.size=10
Vave=NULL
for(i in 1 : (nrow(V)-window.size+ + 1)){
    TEMP=V[i:(i+window.size-1),]
    TEMP=apply(TEMP,2,mean)
    Vave=rbind(Vave,TEMP)
}

#平均速度を保存
data_rename = paste0(data_name,"_Average_Velocity")
save(Vave,file=data_rename)
}
