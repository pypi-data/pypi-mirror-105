import math
import plotly.graph_objects as go
from .Generaldistribution import Distribution

class Gaussian(Distribution):
	""" Gaussian distribution class for calculating and 
	visualizing a Gaussian distribution.
	
	Attributes:
		mean (float) representing the mean value of the distribution
		stdev (float) representing the standard deviation of the distribution
		data_list (list of floats) a list of floats extracted from the data file
			
	"""
	def __init__(self, mu=0, sigma=1):
		
		Distribution.__init__(self, mu, sigma)

	
	def calculate_mean(self):
	
		"""Function to calculate the mean of the data set.
		
		Args: 
			None
		
		Returns: 
			float: mean of the data set
	
		"""
					
		avg = 1.0 * sum(self.data) / len(self.data)
		
		self.mean = avg
		
		return self.mean



	def calculate_stdev(self, sample=True):

		"""Function to calculate the standard deviation of the data set.
		
		Args: 
			sample (bool): whether the data represents a sample or population
		
		Returns: 
			float: standard deviation of the data set
	
		"""

		if sample:
			n = len(self.data) - 1
		else:
			n = len(self.data)
	
		mean = self.mean
	
		sigma = 0
	
		for d in self.data:
			sigma += (d - mean) ** 2
		
		sigma = math.sqrt(sigma / n)
	
		self.stdev = sigma
		
		return self.stdev
		

	def read_data_file(self, file_name, sample=True):
	
		"""Function to read in data from a txt file. The txt file should have
		one number (float) per line. The numbers are stored in the data attribute. 
		After reading in the file, the mean and standard deviation are calculated
				
		Args:
			file_name (string): name of a file to read from
		
		Returns:
			None
		
		"""
			
		with open(file_name) as file:
			data_list = []
			line = file.readline().strip()
			while line:
				data_list.append(int(float(str(line))))
				line = file.readline().strip()
		file.close()
	
		self.data = data_list
		self.mean = self.calculate_mean()
		self.stdev = self.calculate_stdev(sample)

	def plot_histogram(self):
		"""Function to output a histogram of the instance variable data using 
		plotly library.
		
		Args:
			None
			
		Returns:
			None
		"""
			
		x = self.data
		fig = go.Figure(data=[go.Histogram(x=x,  xbins=dict(start=min(x), size=1, end=max(x) + 1))])
		fig.update_layout(xaxis = dict(title = 'Data'),
				yaxis = dict(title = 'Count'), 
				title = 'Histogram of Data')
		fig.show()

	def pdf(self, x):
		"""Probability density function calculator for the gaussian distribution.
		
		Args:
			x (float): point for calculating the probability density function
			
		
		Returns:
			float: probability density function output
		"""
		
		return (1.0 / (self.stdev * math.sqrt(2*math.pi))) * math.exp(-0.5*((x - self.mean) / self.stdev) ** 2)
		

	def plot_histogram_pdf(self, n_spaces = 1000):

		"""Function to plot the normalized histogram of the data and a plot of the 
		probability density function along the same range
		
		Args:
			n_spaces (int): number of data points 
		
		Returns:
			list: x values for the pdf plot
			list: y values for the pdf plot
			
		"""
		
		mu = self.mean
		sigma = self.stdev

		min_range = min(self.data)
		max_range = max(self.data)
		
		 # calculates the interval between x values
		interval = 1.0 * (max_range - min_range) / n_spaces

		x = []
		y = []
		
		# calculate the x values to visualize
		for i in range(n_spaces):
			tmp = min_range + interval*i
			x.append(tmp)
			y.append(self.pdf(tmp))

		fig = go.Figure(data=[go.Histogram(x=self.data, histnorm='probability density', xbins = dict(size = 1),
		 		name = 'Normed histogram')])
		fig.add_trace(go.Scatter(x = x, y = y, mode = 'lines', name = 'Normal distribution'))
		fig.update_layout(xaxis = dict(title = 'Data'),
				yaxis = dict(title = 'Density'), 
				title = 'Normed histogram of Data')
		fig.show()

		return x, y
		
	def __add__(self, other):
		
		"""Function to add together two Gaussian distributions
		
		Args:
			other (Gaussian): Gaussian instance
			
		Returns:
			Gaussian: Gaussian distribution
			
		"""
		
		result = Gaussian()
		result.mean = self.mean + other.mean
		result.stdev = math.sqrt(self.stdev ** 2 + other.stdev ** 2)
		
		return result
		
		
	def __repr__(self):
	
		"""Function to output the characteristics of the Gaussian instance
		
		Args:
			None
		
		Returns:
			string: characteristics of the Gaussian
		
		"""
		
		return "mean {}, standard deviation {}".format(self.mean, self.stdev)