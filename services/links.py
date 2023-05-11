from services.namespace import Namespace

#base_link = "http://172.30.1.152:8080/api/v1/"
# base_link = "http://172.23.32.1:8080/api/v1/"
# base_link = "http://172.28.22.131:8080/api/v1/"
base_link = "http://192.168.0.218:8080/api/v1/"

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
        "single":"task/",
        "project":"task/project/list/" # {projectId} get project task list
    }),
    "taskrole":Namespace({
        "all":"taskrole/all",
        "single":"taskrole/",
        "task":"taskrole/task/",#{taskId}
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
    }),
    "evaluation":Namespace({
        "all":"evaluation/all",
        "single":"evaluation/",
        "position":"evaluation/position/",#{p}
    }),
    "course":Namespace({
        "all":"course/all",
        "single":"course/",
        "position":"course/position/",#{p}
    })
}

links_ns = Namespace(links)
