import pandas as pd
import glob
data_paths = glob.glob('./data/*')
print(data_paths)
df1 = pd.read_csv('./data/bobae.csv')
df2 = pd.read_csv('./data/mlb.csv')

df = pd.concat((df1,df2),sort=False)
#
# df = pd.DataFrame()
# for path in data_paths[1:]:
#     df_temp = pd.read_csv(path, index_col=0)
#     df = pd.concat([df, df_temp], ignore_index=True, axis='rows')
# df_temp = pd.read_csv(data_paths[0])
# df = pd.concat([df, df_temp], ignore_index=True, axis='rows')
# df.info()
df.to_csv('./data/community_t.csv', index=False)
