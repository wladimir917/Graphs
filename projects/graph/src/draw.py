"""
General drawing methods for graphs using Bokeh.
"""

from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import (GraphRenderer, StaticLayoutProvider, Circle, LabelSet,
                          ColumnDataSource)

from random import choice, random, randrange
from functools import reduce
from graph import Graph

class BokehGraph:
  """Class that takes a graph and exposes drawing methods."""
  def __init__(self, graph, title='Graph', width=10, height=10, show_axis=False, show_grid=False, circle_size=35):
    if not graph.vertices:
      raise Exception('Graph should contain vertices!')
    self.graph = graph
    
    # Setup plot
    self.width = width
    self.height = height
    self.pos = {}  # dict to map vertices to x, y positions
    self.plot = figure(title=title, x_range=(0, width), y_range=(0, height))
    self.plot.axis.visible = show_axis
    self.plot.grid.visible = show_grid
    self._setup_graph_renderer(circle_size)

  def _setup_graph_renderer(self, circle_size):
    graph_renderer = GraphRenderer()

    node_indices = [*self.graph.vertices.keys()]

    graph_renderer.node_renderer.data_source.data = dict(
      index=node_indices,
      fill_color=self._get_random_colors())

    graph_renderer.node_renderer.glyph = Circle(size=circle_size, fill_color='fill_color')
    
    graph_renderer.edge_renderer.data_source.data = self._get_edge_indexes()
    self.randomize()

    graph_renderer.layout_provider = StaticLayoutProvider(graph_layout=self.pos)
    self.plot.renderers.append(graph_renderer)

  def _get_edge_indexes(self):
    node_indices = [*self.graph.vertices.keys()]

    return dict(
      start=reduce(lambda x,y: x+y,[[i]*len(self.graph.vertices[i]) for i in node_indices]),
      end=reduce(lambda x,y: x+y,[list(self.graph.vertices[i]) for i in node_indices]))
      
  def _get_random_colors(self):
    colors = []
    for _ in range(len(self.graph.vertices)):
      color = '#'+''.join([choice('0123456789ABCDEF') for j in range(6)])
      colors.append(color)
    return colors

  def randomize(self):
    """Randomize vertex positions."""
    for vertex in self.graph.vertices:
      self.pos[vertex] = (randrange(1,self.width-1),
                          randrange(1,self.height-1))

  def show(self, output_path='./graph.html'):
    output_file(output_path)
    show(self.plot)

test = Graph()  # Instantiate your graph

test.add_vertex('A')
test.add_vertex('B')
test.add_vertex('C')
test.add_vertex('D')
test.add_vertex('E')
test.add_vertex('F')
test.add_vertex('G')
test.add_vertex('H')

test.add_edge('A', 'B')
test.add_edge('A', 'C')
test.add_edge('B', 'H')
test.add_edge('F', 'G')
test.add_edge('C', 'B')
test.add_edge('C', 'D')
test.add_edge('C', 'B')
test.add_edge('H', 'G')


graph = BokehGraph(test)
graph.show()