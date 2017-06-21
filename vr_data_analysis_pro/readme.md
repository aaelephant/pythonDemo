oneStep:
	/Users/qbshen/Work/github/pythonDemo/vr_data_analysis_pro/
	run ftpHandler.py 下载json数据文件
twoStep:
	/Users/qbshen/Work/github/pythonDemo/vr_data_analysis_pro/
	run jsonLoader.py 分离出可用json数据

threeStep:
	/Users/qbshen/Work/github/pythonDemo/vr_data_analysis_pro/promulgator_analysis/analysis_pandas
	run collection_files.py 拼接同一天的json文件到一个文件
fourStep:
	/Users/qbshen/Work/github/pythonDemo/vr_data_analysis_pro/promulgator_analysis/analysis_pandas
	play_statistics.py 播放相关分析脚本


Note:
	json_logs数据在/Users/qbshen/Work/python/Demand/json_logs/
	需要本地mysql数据库，db：vr_bi_statistics  @root pw:123456abc