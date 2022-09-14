def is_date(date_t):
    try:
        date_arr = date_t.split('/')
        #print(date_arr)
        if int(date_arr[0])<32 and int(date_arr[1])<13 and int(date_arr[2])> 2019:
            return True
    except Exception as e:
        print(e)
        return False

def is_greater(date_la, date_ex):
    response1 = is_date(date_la)
    response2 = is_date(date_ex)
    if response1 == response2 == True:
        day_la = int(date_la.split('/')[0])
        day_ex = int(date_ex.split('/')[0])
        # get monts : 
        mont_la = int(date_la.split('/')[1])
        mont_ex = int(date_ex.split('/')[1])
        # get years : 
        year_la = int(date_la.split('/')[2])
        year_ex = int(date_ex.split('/')[2])
        if mont_ex != mont_la and year_la == year_ex:
            if mont_la < mont_ex:
                return True
            else:
                return False
        if year_la == year_ex and mont_la == mont_ex:
            if day_la < day_ex:
                return True
            else:
                return False
        if year_la < year_ex:
            return True
        else:
            return False
    return False