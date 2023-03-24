from services.namespace import Namespace

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