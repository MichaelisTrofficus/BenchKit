from BenchKit.Miscellaneous.User import make_time_series_graph, plot_time_series_point
import concurrent.futures

from .BaseGraph import BenchGraph


class TimeSeries(BenchGraph):

    def __init__(self,
                 graph_name: str,
                 line_names: tuple[str] | str,
                 x_axis_name: str,
                 y_axis_name: str,
                 config_id: dict):

        super().__init__(graph_name, config_id)
        line_names = (line_names,) if isinstance(line_names, str) else line_names

        if len(line_names) > 50:
            raise ValueError("No more than 50 lines can be generated per graph")

        self.line_names = [i.upper() for i in line_names]
        self.x_axis_name = x_axis_name
        self.y_axis_name = y_axis_name
        self.graph_id = None

    def init_graph(self):
        graph_id = make_time_series_graph(self.config_id,
                                          self.graph_name,
                                          self.line_names,
                                          self.x_axis_name,
                                          self.y_axis_name)

        self.graph_id = graph_id

    def log_value(self, *args, **kwargs):

        num_threads = 4

        step = kwargs["step"]

        values = args[0]

        line_name_list = [i.upper() for i in values.keys()]
        graph_id_list = [self.graph_id] * len(line_name_list)
        x_value_list = [step] * len(values)
        y_value_list = list(values.values())

        zips = zip(graph_id_list, line_name_list, x_value_list, y_value_list)

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
            future_results = [executor.submit(plot_time_series_point, *z) for z in zips]

            for future in future_results:
                future.result()
