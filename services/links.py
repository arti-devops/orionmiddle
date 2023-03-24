from services.namespace import Namespace

base_link = "http://localhost:8080/api/v1/"

links = {
    "position":Namespace({
        "all":"position/all",
        "all_active":"position/all/active",
        "single":"position/"
    }),
    "employee":Namespace({
        "all":"employee/all",
        "single":"employee/"
    }),
    "task":Namespace({
        "all":"task/all",
        "single":"task/"
    }),
    "taskrole":Namespace({
        "all":"taskrole/all",
        "single":"taskrole/",
        "position":"taskrole/position/"
    }),
    "logbook":Namespace({
        "all":"logbook/all",
        "range":"logbook/range/", #{s}/{e}
        "prange":"logbook/range/",#{p}/{s}/{e}
        "single":"logbook/"
    }),
    "absence":Namespace({
        "all":"absence/all",
        "range":"absence/range/", #{s}/{e}
        "prange":"absence/range/",#{p}/{s}/{e}
        "single":"absence/"
    })
}

links_ns = Namespace(links)