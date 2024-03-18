total_values = [12.243,3423.25254536,1231231.425245,'null','null']
#our_team(total_values)
def truncate(x):
    if x != 'null':
        return round(x,2)
    else: return x
total_values = [truncate(x) for x in total_values]
print(total_values)