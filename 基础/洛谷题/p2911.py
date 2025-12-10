a,b,c=map(int,input().split())
from collections import defaultdict#！！！！
count = defaultdict(int)#！！！！
for i in range(1,a+1):
    for j in range(1,b+1):
        for k in range(1,c+1):
            s=i+j+k
            count[s]+=1

max_count = max(count.values())
result = min(s for s, cnt in count.items() if cnt == max_count)
print(result)

