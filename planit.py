import datetime
import pygame
import sys
import math
import random
import os
import json

class User:
	user_id = 0;
	name = "";
	password = "";
	tasks = [];

	def __init__ (self, name, password):
		self.name = name;
		self.password = password;
		self.user_id = int(random.random()*1000000);

	def __str__ (self):
		rv = "{";
		rv += "\"user_id\":\""+str(self.user_id)+"\",";
		rv += "\"name\":\""+str(self.name)+"\",";
		rv += "\"password\":\""+str(self.password)+"\"}";
		return rv;

	def draw_tasks(self):
		my_draw_area = DrawArea();

		screen = pygame.display.set_mode(my_draw_area.size);

		for t in self.tasks:
			my_draw_area.tasks.append(t);

		my_draw_area.draw(screen);

		while 1:
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					sys.exit()
				screen.fill((255,255,255))
				my_draw_area.draw(screen);
				pygame.display.flip()

	def save_user (self):
		try:
				os.makedirs("Users/" + str(self.user_id));
		except OSError as e:
			print(e);
			pass;
		for t in self.tasks:
			f = open("Users/" + str(self.user_id) + "/" + str(t.task_id) + ".txt", 'w');
			f.write(str(t));
			f.close();
		f = open("Users/" + str(self.user_id) + "/info.txt", 'w');
		f.write(str(self));
		f.close();

	def load_user (self, iid):
		f = json.loads(open("Users/" + iid + "/info.txt").read());

		self.user_id = f["user_id"];
		self.name = f["name"];
		self.password = f["password"];

		self.tasks = [];
		tasks = os.listdir("Users/" + iid);



class Category:
	user_id = 0;
	name = ""
	color = [128,64,64];

	def __init__ (self):
		self.color = [128,64,64];

	def __str__ (self):
		return str(self.color);

class Task:
	task_id = 0;
	importance = 0;
	user_id = 0;
	label = "";

	# How long it will take and how much is completed
	time_to_complete = 0;
	org_time_to_complete = 0;

	# Allow for an interval to complete in
	start_by_time = 0;
	start_by_date = 0;
	finish_by_date = 0;
	finish_by_time = 0;
	completed = False;

	# If true, never delete from screen
	must_finish = False;

	# Tasks that must be completed after a certain interval
	interval_task = False;
	interval = 0;
	interval_unit = "hour,day,month,week,year";

	# Tasks that must be completed at a certain interval
	recurring = False;
	recurring_interval = 0;
	recurring_interval_unit = "day,month,week,year";
	recurring_interval_selections = [];

	def __init__ (self, user_id):
		self.task_id = int(random.random() * 1000000);
		self.user_id = user_id;
		self.time_to_complete = random.randint(1, 50);
		self.org_time_to_complete = self.time_to_complete + (random.randint(0,3) * 5);
		self.importance = random.randint(1, 5);
		self.category = Category();
		self.start_by_date = self.time_to_complete + random.randint(1,20);
		self.finish_by_date = self.start_by_date;
		self.start_by_time = random.randint(0, 23);
		self.finish_by_time = self.start_by_time;
		self.must_finish = False;
		self.recurring = False;
		self.recurring_interval = 0;

	def __str__ (self):
		rv = "{";
		rv += "'task_id':'" + str(self.task_id) + "',";
		rv += "'user_id':'" + str(self.user_id) + "',";
		rv += "'label':'" + str(self.label) + "',";
		rv += "'time_to_complete':'" + str(self.time_to_complete) + "',";
		rv += "'org_time_to_complete':'" + str(self.org_time_to_complete) + "',";
		rv += "'importance':'" + str(self.importance) + "',";
		rv += "'category':'" + str(self.category) + "',";
		rv += "'start_by_date':'" + str(self.start_by_date) + "',";
		rv += "'finish_by_date':'" + str(self.finish_by_date) + "',";
		rv += "'start_by_time':'" + str(self.start_by_time) + "',";
		rv += "'finish_by_time':'" + str(self.finish_by_time) + "',";
		rv += "'start_by_time':'" + str(self.start_by_time) + "',";
		rv += "'must_finish':'" + str(self.must_finish) + "',";
		rv += "'recurring':'" + str(self.recurring) + "',";
		rv += "'recurring_interval':'" + str(self.recurring_interval) + "'}";
		return rv;


class DrawArea:
	tasks = [];
	size = (640, 480);
	max_circle_size = 60;
	distance_scale = 3;

	def __init__ (self):
		self.tasks = [];
		self.size = (640, 480);

	def draw (self, screen):
		today = 15;
		w = screen.get_width() / 2;
		h = screen.get_height() / 2;

		for t in self.tasks:

			# Fake screen
			surface = pygame.Surface((screen.get_width(), screen.get_height()));
			alpha = int((t.importance / 5.0) * 255);

			surface.fill((255,0,255));
			surface.set_colorkey((255,0,255));

			# Size of circle
			radius = int((t.time_to_complete / 50.0) * self.max_circle_size)
			big_radius = int((t.org_time_to_complete / 50.0) * self.max_circle_size)
			
			# Distance from center
			distance = (t.finish_by_date - today) * self.distance_scale;

			# y-position
			ypos = h/2 + int((t.start_by_time / 24.0) * (h));

			pygame.draw.circle(surface, t.category.color, (w-distance, ypos), radius, 0);
			pygame.draw.circle(surface, t.category.color, (w-distance, ypos), big_radius, 1);

			surface.set_alpha(alpha);

			screen.blit(surface, (0,0));

			myfont = pygame.font.Font(None, 12)
			label = myfont.render(t.label, 1, (0,0,0))

			screen.blit(label, (w-distance-len(t.label)*2, ypos));

pygame.init();

me = User("Cameron","passwd");

task1 = Task(me.user_id);
task2 = Task(me.user_id);
task3 = Task(me.user_id);
task4 = Task(me.user_id);
task5 = Task(me.user_id);
task6 = Task(me.user_id);

task1.label = "Math Homework";
task2.label = "Clean Kitchen";
task3.label = "Job Hunting";
task4.label = "Buy Coffee";
task5.label = "Run Payroll";
task6.label = "Call my Friend";

me.tasks.append(task1);
me.tasks.append(task2);
me.tasks.append(task3);
me.tasks.append(task4);
me.tasks.append(task5);
me.tasks.append(task6);

me.save_user();
me.load_user("786080");

me.draw_tasks();
