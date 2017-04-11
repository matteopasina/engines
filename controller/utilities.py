from datetime import datetime, timedelta


def mapDay(on_day):
    day_of_event = None
    if on_day == 'Monday':
        day_of_event = 0
    elif on_day == 'Tuesday':
        day_of_event = 1
    elif on_day == 'Wednesday':
        day_of_event = 2
    elif on_day == 'Thursday':
        day_of_event = 3
    elif on_day == 'Friday':
        day_of_event = 4
    elif on_day == 'Saturday':
        day_of_event = 5
    elif on_day == 'Sunday':
        day_of_event = 6
    return day_of_event


def convertDatetime(request, template, resource):
    '''
    Converts request.from request.to and template.period in datetimes
    :param resource: a resource class
    :param request: a request class
    :param template: a template class
    :return: 3 datetimes from from_date,to_date and period
    '''
    expirationtime = None
    startime = datetime.strptime(request.from_date, '%d %b %Y')
    endtime = datetime.strptime(request.to_date, '%d %b %Y')
    if resource.to_date != None:
        expirationtime = datetime.strptime(resource.to_date, '%d %b %Y')
    period = timedelta(days=template.period * 7)

    return startime, endtime, period, expirationtime


def shiftMiniplan(miniplan, shift):
    shift = timedelta(days=shift)
    for i in range(0, len(miniplan)):
        miniplan[i].date = miniplan[i].date + shift
    return miniplan


def checkMsgsOneDay(miniplan, endtime):
    '''
    Pops the empty messages from the miniplan(if it has found <nmsg with getlistmessages)
    :param miniplan: a miniplan(list of messages)
    :param endtime: a datetime
    :return: a miniplan(list of messages)
    '''
    c = 0
    for i in range(0, len(miniplan)):
        if miniplan[i].date == None:
            c += 1

        elif miniplan[i].date == miniplan[i - 1].date:
            miniplan[i].date += timedelta(days=1)

            if miniplan[i].date > endtime.date():
                miniplan[i].date -= timedelta(days=1)
                miniplan[i - 1].date -= timedelta(days=1)

    while c > 0:
        miniplan.pop()
        c -= 1

    return miniplan


def rebuildMiniplans(all_messages):
    '''
    This function builds a dictionary with key=miniplan_id given a dictionary that has messages with different miniplan_id
    :param all_messages: dict of messages
    :return: dict of messages with key=miniplan_id
    '''
    miniplans = {}
    for m in all_messages:
        m.date = m.date.date()
        m.time = m.time.time()
        if m.miniplan_id not in miniplans:
            miniplans[m.miniplan_id] = [m]
        else:
            miniplans[m.miniplan_id].append(m)
    return miniplans