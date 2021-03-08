import Dijkstra_with_DLL as dijk
import GUI as gui

# Testing commit and push in githib for VSC


def run(station1, station2, time):
    """Function to run the Dijkstra algorithm and also format the output in a way that can be displayed in the
    interface """
    route = dijk.Dijkstra(station1, station2)
    path_results = route.find_path(dijk.builder(time))
    path = path_results[0]
    total_time = path_results[1]
    lines = dijk.find_lines(path_results[0],time)
    line_ID = lines[0]
    time_taken = lines[1]

    # Headers fot the Table
    records = [('Station', 'Line', 'Travel Time to Next Station(in mins)')]
    # Table Data
    for x, y, z in zip(path, line_ID, time_taken):
        records.append((x, y, z))
    if path_results == "Route Not Possible":
        gui.route_not_possible()
    else:
        gui.results(records, total_time)

