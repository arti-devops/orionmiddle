from services.namespace import Namespace
from services.links import base_link
from services.date import compute_word_days_in_month

def get_direction_name(p):
    p = Namespace(p)
    if p.service is not None:
        subdiv = p.service["subdivision"]
        subdiv = Namespace(subdiv)
        if subdiv.direction is not None:
            return subdiv.direction["shortName"]
        else: return subdiv.shortName
    else:
        div = p.subdivision["direction"]
        if div is not None:
            return div["shortName"]
        else: return p.subdivision["shortName"]

def count_late_occurence(minuteDiffs:list):
    occurences = [1 for t in minuteDiffs if t<0]
    return len(occurences)

def count_no_log_occurence(nb_log:int, date_string:str):
    n_work_days = compute_word_days_in_month(date_string)
    return n_work_days - nb_log

def generate_daterange_link(link, positionId:int, startDate:str, endDate:str):
    """
    Args:
        link (links_ns): A Namespace object created on Link dictionary.
    Returns:
        str: A string representing a full link. 
        i.e: http://172.28.48.1:8080/api/v1/absence/{{s}}/{{e}}.
    """
    return base_link + link.prange + str(positionId) + "/" + startDate + "/" + endDate

def generate_position_req_link(link, p):
    return base_link + link.position + str(p)

def compute_nb_finished_tasks(taskrole):
    finished = [x["task"]["status"] for x in taskrole if x["task"]["status"]=="FINISHED"]
    return len(finished)

def compute_progress(finished:int, nb:int):
    return finished/nb*100