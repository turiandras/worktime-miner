dayOfWeek = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
showEntries = False

class LogEvent:
	def __init__(self,date_string):
		self.date_string = date_string
		self.parse_datestring()
	
	def set_startup(self,startup):
		self.startup = startup
		
	def parse_datestring(self):
		line = self.date_string
		a = line[line.index("D"):len(line)-1]
		t_i = a.index("T")
		self.date = a[6:t_i]
		self.time = a[t_i+1:t_i+6]
	
	def __str__(self):
		type = "Startup" if self.startup else "Shutdown"
		return "%s %s %s" % (self.date, self.time, type)
	
class Time:
	def __init__(self,hour,minute):
		self.hours = int(hour)
		self.minutes = int(minute)
		self.norm()
	
	def norm(self):
		if self.minutes < 0:
			self.minutes = 60+self.minutes
			self.hours -= 1
			self.norm()
		if self.minutes > 60:
			hours_in_min = self.minutes / 60
			self.minutes = self.minutes - hours_in_min*60
			self.hours += hours_in_min
			
	def plus(self,time):
		self.hours += time.hours
		self.minutes += time.minutes
		self.norm()
	
	def divideBy(self,divider):
		min = self.hours*60 + self.minutes
		result_min = min/divider
		result = Time(0,result_min)
		return result
	
	def __str__(self):
		self.norm()
		return str(self.hours)+":"+str(self.minutes)
	
	
def main():
	days = process_input_into_dict_of_lists_of_logevents_groupedby_date()
	times = {}
	lastDayOfWeek = None
	lastDay = None
	for day in sorted(days.iterkeys(),reverse=True):
		if lastDayOfWeek == "Monday":
			calculate_avarage_for_week_starting_on(lastDay,times)
			print ""
			print ""
		lastDayOfWeek = dayOfWeek[string2date(day).weekday()]
		label_for_day = day + " " + lastDayOfWeek
		lastDay = day
		try:
			times[day] = calculate_daily_work_time(days[day])
			print label_for_day, times[day]
			if showEntries:
				for value in days[day]:
					print "\t", value
		except Exception as ex:
			print label_for_day, "bogus daily windows-lifecycle:", ex
			for value in days[day]:
				print "\t", value
				
	# for day in sorted(times.iterkeys(),reverse=True):
		# print day, times[day]
				
def process_input_into_dict_of_lists_of_logevents_groupedby_date():
	f = open("data.dat")
	d = {}
	lastEvent = None
	for line in f:
		if "Date" in line:
			lastEvent = LogEvent(line)
			d.setdefault(lastEvent.date, []).append(lastEvent)
		if "Event ID" in line:
			one_i = line.index("1")
			eventType = line[one_i:one_i+2]
			lastEvent.set_startup(int(eventType) == 12)   # startup:eventID 12, shutdown:eventID 13
	return d
		
def calculate_avarage_for_week_starting_on(day,times):
	from datetime import timedelta
	monday = string2date(day)
	count = 0
	sum = Time(0,0)
	for day in sorted(times.iterkeys()):
		if (string2date(day) - monday) > timedelta(days = 4):
			# we went to far in the future for this week's workdays
			break
		sum.plus(times[day])
		count += 1
		# print "\t\t",day, count, times[day], sum, sum.divideBy(count)
	print "\t\t", "calculated weekly avarage over %d days:" % (count,), sum.divideBy(count), "Total:", sum
	
		
def calculate_daily_work_time(events):
	if len(events) < 2:
		raise Exception("Only one entry")
	if len(events) > 2:
		raise Exception("Too many entries")
	events = sorted(events,reverse=True,key=byTime)
	highest = events[0]
	lowest = events[-1]
	if highest.startup:
		raise Exception("Bogus last daily entry")
	if not lowest.startup:
		raise Exception("Bogus first daily entry")
	hours = int(highest.time[0:2])-int(lowest.time[0:2])
	minutes = int(highest.time[3:5])-int(lowest.time[3:5])
	return Time(hours,minutes)
	
			
def byTime(s):
    return s.time
	
def string2date(str_date):
	from datetime import datetime
	# 2011-09-09 
	date = datetime.strptime(str_date, '%Y-%m-%d')
	return date
	# date_object = datetime.strptime('Jun 1 2005  1:33PM', '%b %d %Y %I:%M%p')
		
if __name__ == '__main__':
	main()
