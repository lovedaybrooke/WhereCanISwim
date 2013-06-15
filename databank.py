# coding=utf-8
lanes = [
    {'pool': 'York Hall Leisure Centre', 'day': 'Monday', 
    'start': '7.00', 'end': '9.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
    'start': '9.00', 'end': '12.20', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
    'start': '12.20', 'end': '13.20', 'descrip': u'♀'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Monday',
    'start': '13.20', 'end':'20.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
    'start': '7.00', 'end': '9.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
    'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
    'start': '12.30', 'end': '13.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
    'start': '13.30', 'end':'15.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Tuesday',
    'start': '15.30', 'end':'17.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
    'start': '7.00', 'end': '9.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
    'start': '9.00', 'end': '12.20', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
    'start': '12.20', 'end': '13.20', 'descrip': u'♀'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Wednesday',
    'start': '13.30', 'end':'17.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
    'start': '7.00', 'end': '9.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
    'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
    'start': '12.30', 'end': '13.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
    'start': '13.30', 'end':'19.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Thursday',
    'start': '19.30', 'end': '21.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
    'start': '7.00', 'end': '9.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
    'start': '9.00', 'end': '12.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
    'start': '12.30', 'end': '13.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
    'start': '13.30', 'end':'15.30', 'descrip': 'Shared with school'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Friday',
    'start': '15.30', 'end': '17.30'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Saturday',
    'start': '8.00', 'end': '12.00'},
    {'pool': 'York Hall Leisure Centre', 'day': 'Sunday',
    'start': '8.00', 'end': '15.30'},
    {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '6.30',
    'end': '10.15'},
    {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '10.15',
    'end': '12.15', 'descrip': u'♀'},
    {'pool': 'Mile End Pools', 'day': 'Monday', 'start': '12.15',
    'end': '22.00'},
    {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '6.30',
    'end': '13.30'},
    {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '13.30',
    'end': '15.30', 'descrip': u'♀'},
    {'pool': 'Mile End Pools', 'day': 'Tuesday', 'start': '15.30',
    'end': '22.00'},
    {'pool': 'Mile End Pools', 'day': 'Wednesday', 'start': '6.30',
    'end': '22.00'},
    {'pool': 'Mile End Pools', 'day': 'Thursday', 'start': '6.30',
    'end': '19.00'},
    {'pool': 'Mile End Pools', 'day': 'Thursday', 'start': '19.00',
    'end': '22.00', 'descrip': u'♀'},
    {'pool': 'Mile End Pools', 'day': 'Friday', 'start': '6.30',
    'end': '22.00'},
    {'pool': 'Mile End Pools', 'day': 'Saturday', 'start': '9.00',
    'end': '17.00'},
    {'pool': 'Mile End Pools', 'day': 'Sunday', 'start': '9.00',
    'end': '17.00'},
    {'pool': 'Ironmonger Row', 'day': 'Monday', 'start': '6.30',
    'end': '21.30'},
    {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '6.30',
    'end': '14.00'},
    {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '14.00',
    'end': '15.00', 'descrip': 'Shared with school'},
    {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '15.00',
    'end': '19.30'},
    {'pool': 'Ironmonger Row', 'day': 'Tuesday', 'start': '19.30',
    'end': '21.30', 'descrip': u'♀'},
    {'pool': 'Ironmonger Row', 'day': 'Wednesday', 'start': '6.30',
    'end': '21.30'},
    {'pool': 'Ironmonger Row', 'day': 'Thursday', 'start': '6.30',
    'end': '20.00'},
    {'pool': 'Ironmonger Row', 'day': 'Friday', 'start': '6.30',
    'end': '19.00'},
    {'pool': 'Ironmonger Row', 'day': 'Saturday', 'start': '9.00',
    'end': '10.00'},
    {'pool': 'Ironmonger Row', 'day': 'Saturday', 'start': '10.00',
    'end': '18.00', 'descrip': 'Shared with fun swim'},
    {'pool': 'Ironmonger Row', 'day': 'Sunday', 'start': '9.00',
    'end': '10.00'},
    {'pool': 'Ironmonger Row', 'day': 'Sunday', 'start': '10.00',
    'end': '18.00', 'descrip': 'Shared with fun swim'},
    {'pool': 'London Fields Lido', 'day': 'Monday', 'start': '6.30',
    'end': '20.00'},
    {'pool': 'London Fields Lido', 'day': 'Tuesday', 'start': '6.30',
    'end': '19.00'},
    {'pool': 'London Fields Lido', 'day': 'Tuesday', 'start': '19.00',
    'end': '20.00', 'descrip': u'♀'},
    {'pool': 'London Fields Lido', 'day': 'Wednesday', 'start': '6.30',
    'end': '19.00'},
    {'pool': 'London Fields Lido', 'day': 'Thursday', 'start': '6.30',
    'end': '20.00'},
    {'pool': 'London Fields Lido', 'day': 'Friday', 'start': '6.30',
    'end': '20.00'},
    {'pool': 'London Fields Lido', 'day': 'Saturday', 'start': '8.00',
    'end': '10.00'},
    {'pool': 'London Fields Lido', 'day': 'Saturday', 'start': '10.00',
    'end': '17.00', 'descrip': 'Shared with fun swim'},
    {'pool': 'London Fields Lido', 'day': 'Sunday', 'start': '8.00',
    'end': '10.00'},
    {'pool': 'London Fields Lido', 'day': 'Sunday', 'start': '10.00',
    'end': '17.00', 'descrip': 'Shared with fun swim'}
    ]