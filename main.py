from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.animation import Animation
from kivy.core.audio import SoundLoader

from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.behaviors.button import ButtonBehavior
from kivy.uix.image import Image 
from kivy.uix.label import Label

try:
	import requests               #импорт requests для подключения к API
except:                           #в скомпилированном приложении API не работает (статус работы отображается в верхней части экрана)
	pass                          #но работает при запуске кода

class AnButt(ButtonBehavior, Image):       #классы кнопок
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.source = 'butn.png'

class NaButt(ButtonBehavior, Image):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.source = 'ntub.png'

class Number(ButtonBehavior, Image):
	def __init__(self, num, **kwargs):
		super().__init__(**kwargs)
		self.source = f'{str(num)}.png'
		self.num = num
#разерешение экрана в скомпилированном приложении не установлено, строчка добавлена для корректного запуска кода
#размеры виджетов подстраиваются под разрешение экрана
#Window.size = (540, 960)                
Window.clearcolor = (1, 1, 1, 1)
class ConvApp(App):
	try:                 #подключение к API
		RATES = {
		'EUR' : requests.get('https://api.exchangeratesapi.io/latest').json()["rates"],
		'JPY' : requests.get('https://api.exchangeratesapi.io/latest?base=JPY').json()["rates"],
		'RUB' : requests.get('https://api.exchangeratesapi.io/latest?base=RUB').json()["rates"],
		'USD' : requests.get('https://api.exchangeratesapi.io/latest?base=USD').json()["rates"],
		'GBP' : requests.get('https://api.exchangeratesapi.io/latest?base=GBP').json()["rates"]}
	except:   #при отсутствии доступа переход к фиксированным значениям
		text = 'Конвертация валют   (Нет доступа к API)'
		RATES = {
		 'EUR': {'RUB': 77.0563, 'JPY': 123.41, 'USD': 1.1285, 'GBP': 0.89173}, 
		 'JPY': {'GBP': 0.0072257516,'RUB': 0.6243926748,'EUR': 0.0081030711,'USD': 0.0091443157},
		 'RUB': {'GBP': 0.0115724477, 'JPY': 1.6015562647, 'EUR': 0.0129775242, 'USD': 0.0146451361}, 
		 'USD': {'GBP': 0.7901905184, 'RUB': 68.2820558263, 'JPY': 109.3575542756, 'EUR': 0.8861320337}, 
		 'GBP': {'RUB': 86.4121426889, 'JPY': 138.3939084701, 'EUR': 1.1214156751, 'USD': 1.2655175894}}
	else:
		text = 'Конвертация валют   (Доступ к API)'


	def build(self):
		#обновление конфигураций при запуске приложения
		self.config.set('val', 'first',	'RUB')
		self.config.update_config('conv.ini')
		self.config.set('val', 'second', 'USD')
		self.config.update_config('conv.ini')

		self.sound = SoundLoader.load('sound.wav') #звук нажатия кнопок

		flt = FloatLayout(size_hint = (1, 1))       #основной виджет экрана
		#виджеты располагаются в порядке сверху вниз
		self.top_btn = Button(disabled = True, size_hint = (1, .07), background_color = (.42, .68, .87, 1), background_disabled_normal = '', pos_hint = {'top':1},
							  text = self.text, font_size = '14sp', font_name = 'arial.ttf')
		flt.add_widget(self.top_btn)
		#значения переводимой валюты и итог
		bxl_btn = Button(size_hint = (1, .15), pos_hint = {'top':.90}, disabled = True, background_color = (.42, .68, .87, 1), background_disabled_normal = '')
		bxl = GridLayout(size_hint = (1, .15), pos_hint = {'top':.90}, cols = 2, rows = 2)
		x = Window.size[0] * 0.77
		y = Window.size[1] * 0.066
		self.lbl_1 = Label(text = '0', color = (.8, .8, .8, 1), font_size = '32sp', font_name = 'MilanoFont.ttf', size_hint = (.9, .5), 
						   halign = 'left', text_size = (x, y))
		self.zn_1 = Label(text = '₽', font_size = '32sp', size_hint = (.1, .5))
		self.lbl_2 = Label(text = '0', color = (.8, .8, .8, 1), font_size = '32sp', font_name = 'MilanoFont.ttf', 
						    size_hint = (.9, .5), halign = 'left', disabled = True, text_size = (x, y))
		self.zn_2 = Label(text = '$', font_size = '32sp', size_hint = (.1, .5))
		bxl.add_widget(self.lbl_1)
		bxl.add_widget(self.zn_1)
		bxl.add_widget(self.lbl_2)
		bxl.add_widget(self.zn_2)
		flt.add_widget(bxl_btn)
		flt.add_widget(bxl)
		#левая выезжающая кнопка выбора валюты
		self.l_btn = AnButt(size_hint = (1.01, .15), pos_hint = {'top':.75, 'center_x':-.25}, on_press = self.anim_l)
		self.bx_l = BoxLayout(size_hint = (1, .15), pos_hint = {'top':.75, 'center_x':-.25}) #виджет, содержащий в себе отдельные кнопки валют
		self.lb_1 = Label(size_hint = (.2, 1), text = '€', color = (.9, .9, .9, 1), font_size = '28sp')
		self.lb_2 = Label(size_hint = (.2, 1), text = '$', color = (.9, .9, .9, 1), font_size = '28sp')
		self.lb_3 = Label(size_hint = (.2, 1), text = '¥', color = (.9, .9, .9, 1), font_size = '28sp')
		self.lb_4 = Label(size_hint = (.2, 1), text = '£', color = (.9, .9, .9, 1), font_size = '28sp')
		self.lb_5 = Label(size_hint = (.2, 1), text = '₽', font_size = '28sp')
		n = [self.lb_1, self.lb_2, self.lb_3, self.lb_4, self.lb_5]
		for i in n:
			self.bx_l.add_widget(i)
		flt.add_widget(self.l_btn)
		flt.add_widget(self.bx_l)
		#правая выезжающая кнопка выбора валюты
		self.r_btn = NaButt(size_hint = (1.01, .15), pos_hint = {'top':.75, 'center_x':1.25}, on_press = self.anim_r)
		self.bx_r = BoxLayout(size_hint = (1, .15), pos_hint = {'top':.75, 'center_x':1.25})
		self.rb_1 = Label(size_hint = (.2, 1), text = '$', font_size = '28sp')
		self.rb_2 = Label(size_hint = (.2, 1), text = '₽', color = (.9, .9, .9, 1), font_size = '28sp')
		self.rb_3 = Label(size_hint = (.2, 1), text = '¥', color = (.9, .9, .9, 1), font_size = '28sp')
		self.rb_4 = Label(size_hint = (.2, 1), text = '£', color = (.9, .9, .9, 1), font_size = '28sp')
		self.rb_5 = Label(size_hint = (.2, 1), text = '€', color = (.9, .9, .9, 1), font_size = '28sp')
		n = [self.rb_1, self.rb_2, self.rb_3, self.rb_4, self.rb_5]
		for i in n:
			self.bx_r.add_widget(i)
		flt.add_widget(self.r_btn)
		flt.add_widget(self.bx_r)
		#кнопка 'OK'
		self.ok = Number(num = 'ok', size_hint = (.2, .2), pos_hint = {'center_x':0.5, 'top':.67}, on_press = self.ok_press)
		flt.add_widget(self.ok)
		#сетка калькулятора
		self.grl = GridLayout(size_hint = (1, .45), pos_hint = {'top':.47}, cols = 3, rows = 4, spacing = 10, padding = -5)
		self.grl.add_widget(Number(num = 7, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 8, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 9, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 4, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 5, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 6, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 1, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 2, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 3, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 'p', size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 0, size_hint = (.3, .4), on_press = self.numbers))
		self.grl.add_widget(Number(num = 'b', size_hint = (.3, .4), on_press = self.numbers))
		flt.add_widget(self.grl)

		return flt
	#создание файла конфигураций для определения конвертируемых валют
	def build_config(self, config):
		config.setdefaults('val', {'first':'RUB', 'second':'USD'})
		Window.bind(on_touch_down = self.touch_down)

	dct = {'₽':'RUB', '€':'EUR', '$':'USD', '¥':'JPY', '£':'GBP'}
	#словарь нужен, так как для конфигураций нельзя использовать символы обозначения валют   
	def touch_down(self, obj, t):
		#работа левой кнопки выбора валют
		if self.bx_l.collide_point(*t.pos):
			if self.lb_1.collide_point(*t.pos):
				self.lb_1.text, self.lb_5.text = self.lb_5.text, self.lb_1.text
			elif self.lb_2.collide_point(*t.pos):
				self.lb_2.text, self.lb_5.text = self.lb_5.text, self.lb_2.text
			elif self.lb_3.collide_point(*t.pos):
				self.lb_3.text, self.lb_5.text = self.lb_5.text, self.lb_3.text
			elif self.lb_4.collide_point(*t.pos):
				self.lb_4.text, self.lb_5.text = self.lb_5.text, self.lb_4.text
			#изменение конфигураций после выбора валюты
			self.zn_1.text = self.lb_5.text
			self.config.set('val', 'first', self.dct[self.lb_5.text])
			self.config.update_config('conv.ini')
		#работа правой кнопки выбора валют
		if self.bx_r.collide_point(*t.pos):
			if self.rb_2.collide_point(*t.pos):
				self.rb_1.text, self.rb_2.text = self.rb_2.text, self.rb_1.text
			elif self.rb_3.collide_point(*t.pos):
				self.rb_1.text, self.rb_3.text = self.rb_3.text, self.rb_1.text
			elif self.rb_4.collide_point(*t.pos):
				self.rb_1.text, self.rb_4.text = self.rb_4.text, self.rb_1.text
			elif self.rb_5.collide_point(*t.pos):
				self.rb_1.text, self.rb_5.text = self.rb_5.text, self.rb_1.text
			#изменение конфигураций после выбора валюты
			self.zn_2.text = self.rb_1.text
			self.config.set('val', 'second', self.dct[self.rb_1.text])
			self.config.update_config('conv.ini')
	#нажатие кнопки 'OK' и подсчёт значения
	m = 0 #счётчик для изменения статуса работы в верхней части экрана 
	def ok_press(self, btn):
		self.sound.play()
		#значения для конвертации берутся из конфигураций 
		vl_1 = self.config.get('val', 'first')
		vl_2 = self.config.get('val', 'second')
		try:
			sm = float(self.lbl_1.text) #отлов исключений при некорректном вводе
		except:
			self.top_btn.text = 'Введите корректное число'
			self.m = 1
		else:
			if self.m:
				self.top_btn.text = self.text
				self.m = 0
			if vl_1 == vl_2:
				self.lbl_2.text = self.lbl_1.text
			else:
				if sm:
					self.lbl_2.text = '%.2f' % (self.RATES[vl_1][vl_2] * sm)
					self.lbl_2.color = (1, 1, 1, 1)
				else:
					self.lbl_2.text = '0'
					self.lbl_2.color = (.8, .8, .8, 1)


	#анимация левой кнопки валют
	k = 1
	def anim_l(self, btn):

		self.sound.play()

		if self.k % 2 == 1:
			#сдвиг правой кнопки для освобождения места                                             
			an = Animation(pos_hint = {'center_x':1.76}, duration = .2)
			an.start(self.r_btn)
			an.start(self.bx_r)
			an = Animation(pos_hint = {'center_x':.49}, duration = .2) #сдвиг левой кнопки
			an.start(btn)
			an.start(self.bx_l)
			self.k += 1
		else:
			an = Animation(pos_hint = {'center_x':1.25}, duration = .2)
			an.start(self.r_btn)
			an.start(self.bx_r)
			an = Animation(pos_hint = {'center_x':-.25}, duration = .2)
			an.start(btn)
			an.start(self.bx_l)
			self.k += 1
	#анимация правой кнопки валют
	n = 1
	def anim_r(self, btn):
		
		self.sound.play()

		if self.n % 2 == 1:
			an = Animation(pos_hint = {'center_x':-.51}, duration = .2)
			an.start(self.l_btn)
			an.start(self.bx_l)
			an = Animation(pos_hint = {'center_x':.51}, duration = .2)
			an.start(btn)
			an.start(self.bx_r)
			self.n += 1
		else:
			an = Animation(pos_hint = {'center_x':-.25}, duration = .2)
			an.start(self.l_btn)
			an.start(self.bx_l)
			an = Animation(pos_hint = {'center_x':1.25}, duration = .2)
			an.start(btn)
			an.start(self.bx_r)
			self.n += 1 
	#калькулятор
	def numbers(self, btn):
		self.sound.play()
		if btn.num == 'p':
			if self.lbl_1.text == '0':
				self.lbl_1.color = (1, 1, 1, 1)
			self.lbl_1.text += '.'
		elif btn.num == 'b':
			self.lbl_1.text = self.lbl_1.text[:-1]
			if self.lbl_1.text == '':
				self.lbl_1.text = '0'
				self.lbl_1.color = (.8, .8, .8, 1)
		else:
			if self.lbl_1.text == '0':
				self.lbl_1.color = (1, 1, 1, 1)
				self.lbl_1.text = ''
				self.lbl_1.text += str(btn.num)
			else:
				self.lbl_1.text += str(btn.num)


if __name__ == '__main__':
	ConvApp().run()
